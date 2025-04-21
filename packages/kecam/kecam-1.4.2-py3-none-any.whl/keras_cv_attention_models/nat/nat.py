import numpy as np
from keras_cv_attention_models import backend
from keras_cv_attention_models.backend import layers, models, functional, initializers, image_data_format
from keras_cv_attention_models.models import register_model
from keras_cv_attention_models.attention_layers import (
    add_with_layer_scale_and_drop_block,
    ChannelAffine,
    CompatibleExtractPatches,
    conv2d_no_bias,
    drop_block,
    layer_norm,
    mlp_block,
    output_block,
    add_pre_post_process,
)
from keras_cv_attention_models.download_and_load import reload_model_weights

PRETRAINED_DICT = {
    "nat_base": {"imagenet": "d221eaec4af71dd3522625333aa73d9e"},
    "nat_mini": {"imagenet": "921de737ccebe4ab210dcd79ec0aed5f"},
    "nat_small": {"imagenet": "5716d0d54f3abd582e586fbdea04b3db"},
    "nat_tiny": {"imagenet": "91ed860ca950de181f433c189135070b"},
    "dinat_base": {"imagenet": "fcd60313a2d579542bfce3ffbc32c216"},
    "dinat_large": {
        "imagenet21k-ft1k": {224: "4be0fd03d4abba37ac815184017ac197", 384: "52b5397af0d337e2f366e41d34ad9c90"},
        "imagenet21k": "e09f6fe4d39289c25b1280a2d100341f",
    },
    "dinat_large_k11": {"imagenet21k-ft1k": "8874a98e3c6a37ce57499b3f91e918a0"},
    "dinat_mini": {"imagenet": "155c369909fbc6b19f22f2702deb42b5"},
    "dinat_small": {"imagenet": "879cf023c5c85f17c6f30c7f070fc13f"},
    "dinat_tiny": {"imagenet": "c9b15d1862f0eb2eaa6b7e70d3ea0d46"},
}


@backend.register_keras_serializable(package="kecam/nat")
class MultiHeadRelativePositionalKernelBias(layers.Layer):
    def __init__(self, input_height=-1, is_heads_first=False, dilation_rate=1, **kwargs):
        super().__init__(**kwargs)
        self.input_height, self.is_heads_first, self.dilation_rate = input_height, is_heads_first, dilation_rate

    def _pad_bias_(self, indexes, total, dilation_rate):
        size = indexes.shape[0]

        bias_left = np.repeat(indexes[: size // 2], dilation_rate)
        bias_right = np.repeat(indexes[size // 2 + 1 :], dilation_rate)
        bias_center = np.repeat(indexes[size // 2], total - bias_left.shape[0] - bias_right.shape[0])
        return np.concatenate([bias_left, bias_center, bias_right], axis=-1)

    def build(self, input_shape):
        # input (is_heads_first=False): `[batch, height * width, num_heads, ..., size * size]`
        # input (is_heads_first=True): `[batch, num_heads, height * width, ..., size * size]`
        blocks, num_heads = (input_shape[2], input_shape[1]) if self.is_heads_first else (input_shape[1], input_shape[2])
        size = int(np.sqrt(float(input_shape[-1])))
        height = self.input_height if self.input_height > 0 else int(np.sqrt(float(blocks)))
        width = blocks // height
        pos_size = 2 * size - 1
        initializer = initializers.truncated_normal(stddev=0.02)
        self.pos_bias = self.add_weight(name="positional_embedding", shape=(num_heads, pos_size * pos_size), initializer=initializer, trainable=True)

        dilation_rate = self.dilation_rate if isinstance(self.dilation_rate, (list, tuple)) else (self.dilation_rate, self.dilation_rate)
        idx_hh, idx_ww = np.arange(0, size), np.arange(0, size)
        coords = np.reshape(np.expand_dims(idx_hh, -1) * pos_size + idx_ww, [-1]).astype("int64")
        bias_hh = self._pad_bias_(idx_hh, total=height, dilation_rate=dilation_rate[0])
        bias_ww = self._pad_bias_(idx_ww, total=width, dilation_rate=dilation_rate[1])

        bias_hw = np.expand_dims(bias_hh, -1) * pos_size + bias_ww
        bias_coords = np.expand_dims(bias_hw, -1) + coords
        bias_coords = np.reshape(bias_coords, [-1, size**2])[::-1]  # torch.flip(bias_coords, [0])

        bias_coords_shape = [bias_coords.shape[0]] + [1] * (len(input_shape) - 4) + [bias_coords.shape[1]]
        bias_coords = np.reshape(bias_coords, bias_coords_shape)  # [height * width, 1 * n, size * size]
        if hasattr(self, "register_buffer"):  # PyTorch
            self.register_buffer("bias_coords", functional.convert_to_tensor(bias_coords.copy(), dtype="int64"), persistent=False)
        else:
            self.bias_coords = functional.convert_to_tensor(bias_coords, dtype="int64")

        if not self.is_heads_first:
            self.transpose_perm = [1, 0] + list(range(2, len(input_shape) - 1))  # transpose [num_heads, height * width] -> [height * width, num_heads]

    def call(self, inputs):
        if self.is_heads_first:
            return inputs + functional.gather(self.pos_bias, self.bias_coords, axis=-1)
        else:
            return inputs + functional.transpose(functional.gather(self.pos_bias, self.bias_coords, axis=-1), self.transpose_perm)

    def get_config(self):
        base_config = super().get_config()
        base_config.update({"input_height": self.input_height, "is_heads_first": self.is_heads_first, "dilation_rate": self.dilation_rate})
        return base_config


def replicate_padding(inputs, kernel_size=1, dilation_rate=1):
    padded = (kernel_size - 1) // 2
    dilation_rate = dilation_rate if isinstance(dilation_rate, (list, tuple)) else (dilation_rate, dilation_rate)

    if backend.is_torch_backend and max(dilation_rate) == 1:  # NAT
        out = functional.pad(inputs, paddings=[[padded, padded], [padded, padded], [0, 0]], mode="replicate")
    elif backend.is_torch_backend:  # DiNAT
        paddings = [[dilation_rate[0], dilation_rate[0]], [dilation_rate[1], dilation_rate[1]], [0, 0]]
        out = inputs
        for _ in range(padded):
            out = functional.pad(out, paddings=paddings, mode="replicate")
    elif max(dilation_rate) == 1:  # TF NAT
        nn = functional.concat([functional.repeat(inputs[:, :1], padded, axis=1), inputs, functional.repeat(inputs[:, -1:], padded, axis=1)], axis=1)
        out = functional.concat([functional.repeat(nn[:, :, :1], padded, axis=2), nn, functional.repeat(nn[:, :, -1:], padded, axis=2)], axis=2)
    else:  # TF DiNAT
        # left = functional.repeat(functional.expand_dims(inputs[:, :dilation_rate], axis=1), padded, axis=1)
        # left = functional.reshape(left, [-1, left.shape[1] * left.shape[2], *left.shape[2:]])
        multiples = [padded if id == 1 else 1 for id in range(len(inputs.shape))]
        top = functional.tile(inputs[:, : dilation_rate[0]], multiples)
        bottom = functional.tile(inputs[:, -dilation_rate[0] :], multiples)
        top_bottom = functional.concat([top, inputs, bottom], axis=1)

        multiples = [padded if id == 2 else 1 for id in range(len(inputs.shape))]
        left = functional.tile(top_bottom[:, :, : dilation_rate[1]], multiples)
        right = functional.tile(top_bottom[:, :, -dilation_rate[1] :], multiples)
        out = functional.concat([left, top_bottom, right], axis=2)
    return out


def neighborhood_attention(
    inputs, kernel_size=7, num_heads=4, key_dim=0, out_weight=True, qkv_bias=True, out_bias=True, dilation_rate=1, attn_dropout=0, output_dropout=0, name=None
):
    _, hh, ww, cc = inputs.shape
    key_dim = key_dim if key_dim > 0 else cc // num_heads
    qk_scale = 1.0 / (float(key_dim) ** 0.5)
    out_shape = cc
    qkv_out = num_heads * key_dim
    dilation_rate = dilation_rate if isinstance(dilation_rate, (list, tuple)) else (dilation_rate, dilation_rate)
    # print(f"{dilation_rate = }, {kernel_size = }, {inputs.shape = }")

    window_size = [int(kernel_size * ii) for ii in dilation_rate]
    # window_size = int(kernel_size + (kernel_size - 1) * (dilation_rate - 1))
    should_pad_hh, should_pad_ww = max(0, window_size[0] - hh), max(0, window_size[1] - ww)
    if should_pad_hh or should_pad_ww:
        inputs = functional.pad(inputs, [[0, 0], [0, should_pad_hh], [0, should_pad_ww], [0, 0]])
        _, hh, ww, cc = inputs.shape

    qkv = layers.Dense(qkv_out * 3, use_bias=qkv_bias, name=name and name + "qkv")(inputs)
    query, key_value = functional.split(qkv, [qkv_out, qkv_out * 2], axis=-1)  # Matching weights from PyTorch
    query = functional.expand_dims(functional.reshape(query, [-1, hh * ww, num_heads, key_dim]), -2)  # [batch, hh * ww, num_heads, 1, key_dim]

    # key_value: [batch, height - (kernel_size - 1), width - (kernel_size - 1), kernel_size, kernel_size, key + value]
    # print(f"{key_value.shape = }, {window_size = }")
    if backend.is_torch_backend:
        key_value = functional.extract_patches(key_value, sizes=kernel_size, strides=1, rates=dilation_rate, padding="valid", compressed=True)
        key_value = replicate_padding(key_value, kernel_size=kernel_size, dilation_rate=dilation_rate)  # Keep it here, as the input shape is different
    else:
        key_value = CompatibleExtractPatches(sizes=kernel_size, strides=1, rates=dilation_rate, padding="valid", compressed=False)(key_value)
        key_value = replicate_padding(key_value, kernel_size=kernel_size, dilation_rate=dilation_rate)
    # print(f"After pad {key_value.shape = }")

    key_value = functional.reshape(key_value, [-1, kernel_size * kernel_size, qkv_out * 2])
    key, value = functional.split(key_value, 2, axis=-1)  # [batch * block_height * block_width, K * K, key_dim]
    # print(f"{key.shape = }, {value.shape = }, {[hh * ww, num_heads, key_dim, kernel_size * kernel_size] = }")
    key = functional.transpose(functional.reshape(key, [-1, key.shape[1], num_heads, key_dim]), [0, 2, 3, 1])  # [batch * hh*ww, num_heads, key_dim, K * K]
    key = functional.reshape(key, [-1, hh * ww, num_heads, key_dim, kernel_size * kernel_size])  # [batch, hh*ww, num_heads, key_dim, K * K]
    value = functional.transpose(functional.reshape(value, [-1, value.shape[1], num_heads, key_dim]), [0, 2, 1, 3])
    value = functional.reshape(value, [-1, hh * ww, num_heads, kernel_size * kernel_size, key_dim])  # [batch, hh*ww, num_heads, K * K, key_dim]
    # print(f">>>> {query.shape = }, {key.shape = }, {value.shape = }")

    # [batch, hh * ww, num_heads, 1, kernel_size * kernel_size]
    attention_scores = (query @ key) * qk_scale
    attention_scores = MultiHeadRelativePositionalKernelBias(input_height=hh, dilation_rate=dilation_rate, name=name and name + "pos")(attention_scores)
    attention_scores = layers.Softmax(axis=-1, name=name and name + "attention_scores")(attention_scores)
    attention_scores = layers.Dropout(attn_dropout, name=name and name + "attn_drop")(attention_scores) if attn_dropout > 0 else attention_scores

    # attention_output = [batch, block_height * block_width, num_heads, 1, key_dim]
    attention_output = attention_scores @ value
    attention_output = functional.reshape(attention_output, [-1, hh, ww, num_heads * key_dim])
    # print(f">>>> {attention_output.shape = }, {attention_scores.shape = }")

    if should_pad_hh or should_pad_ww:
        attention_output = attention_output[:, : hh - should_pad_hh, : ww - should_pad_ww, :]

    if out_weight:
        # [batch, hh, ww, num_heads * key_dim] * [num_heads * key_dim, out] --> [batch, hh, ww, out]
        attention_output = layers.Dense(out_shape, use_bias=out_bias, name=name and name + "output")(attention_output)
    attention_output = layers.Dropout(output_dropout, name=name and name + "out_drop")(attention_output) if output_dropout > 0 else attention_output
    return attention_output


def nat_block(
    inputs, attn_kernel_size=7, num_heads=4, mlp_ratio=4, dilation_rate=1, attn_drop_rate=0, drop_rate=0, layer_scale=-1, activation="gelu", name=None
):
    input_channel = inputs.shape[-1]
    attn = layer_norm(inputs, axis=-1, name=name + "attn_")
    attn = neighborhood_attention(attn, attn_kernel_size, num_heads, dilation_rate=dilation_rate, attn_dropout=attn_drop_rate, name=name + "attn_")
    attn_out = add_with_layer_scale_and_drop_block(inputs, attn, layer_scale=layer_scale, drop_rate=drop_rate, axis=-1, name=name + "1_")

    mlp = layer_norm(attn_out, axis=-1, name=name + "mlp_")
    mlp = mlp_block(mlp, int(input_channel * mlp_ratio), activation=activation, name=name + "mlp_")
    return add_with_layer_scale_and_drop_block(attn_out, mlp, layer_scale=layer_scale, drop_rate=drop_rate, axis=-1, name=name + "2_")


def NAT(
    num_blocks=[3, 4, 6, 5],
    out_channels=[64, 128, 256, 512],
    num_heads=[2, 4, 8, 16],
    stem_width=-1,
    attn_kernel_size=7,
    use_every_other_dilations=False,  # True for DiNAT, using `dilation_rate=nn.shape[1] // attn_kernel_size` in every other attention blocks
    mlp_ratio=3,
    layer_scale=-1,
    input_shape=(224, 224, 3),
    activation="gelu",
    num_classes=1000,
    drop_connect_rate=0,
    classifier_activation="softmax",
    dropout=0,
    pretrained=None,
    model_name="nat",
    kwargs=None,
):
    """ConvTokenizer stem"""
    # Regard input_shape as force using original shape if len(input_shape) == 4,
    # else assume channel dimension is the one with min value in input_shape, and put it first or last regarding image_data_format
    input_shape = backend.align_input_shape_by_image_data_format(input_shape)
    inputs = layers.Input(input_shape)
    stem_width = stem_width if stem_width > 0 else out_channels[0]
    nn = conv2d_no_bias(inputs, stem_width // 2, kernel_size=3, strides=2, use_bias=True, padding="same", name="stem_1_")
    nn = conv2d_no_bias(nn, stem_width, kernel_size=3, strides=2, use_bias=True, padding="same", name="stem_2_")
    nn = nn if image_data_format() == "channels_last" else layers.Permute([2, 3, 1])(nn)  # channels_first -> channels_last
    nn = layer_norm(nn, axis=-1, name="stem_")

    """ stages """
    total_blocks = sum(num_blocks)
    global_block_id = 0
    for stack_id, (num_block, out_channel, num_head) in enumerate(zip(num_blocks, out_channels, num_heads)):
        stack_name = "stack{}_".format(stack_id + 1)
        if stack_id > 0:
            ds_name = stack_name + "downsample_"
            nn = nn if image_data_format() == "channels_last" else layers.Permute([3, 1, 2])(nn)  # channels_last -> channels_first
            nn = conv2d_no_bias(nn, out_channel, kernel_size=3, strides=2, padding="same", name=ds_name)
            nn = nn if image_data_format() == "channels_last" else layers.Permute([2, 3, 1])(nn)  # channels_first -> channels_last
            nn = layer_norm(nn, axis=-1, name=ds_name)
        for block_id in range(num_block):
            block_name = stack_name + "block{}_".format(block_id + 1)
            drop_rate = drop_connect_rate * global_block_id / total_blocks
            if use_every_other_dilations and block_id % 2 == 1:
                # input 224 kernel_size 7 -> [8, 4, 2 ,1], input 384 kernel_size 7 -> [13, 6, 3 ,1], input 384 kernel_size 11 -> [8, 4, 2, 1]
                dilation_rate = (max(1, int(nn.shape[1] // attn_kernel_size)), max(1, int(nn.shape[2] // attn_kernel_size)))
            else:
                dilation_rate = 1
            nn = nat_block(
                nn, attn_kernel_size, num_head, mlp_ratio, dilation_rate, drop_rate=drop_rate, layer_scale=layer_scale, activation=activation, name=block_name
            )
            global_block_id += 1
    nn = layer_norm(nn, axis=-1, name="pre_output_")
    nn = nn if image_data_format() == "channels_last" else layers.Permute([3, 1, 2])(nn)  # channels_last -> channels_first

    nn = output_block(nn, num_classes=num_classes, drop_rate=dropout, classifier_activation=classifier_activation)
    model = models.Model(inputs, nn, name=model_name)
    add_pre_post_process(model, rescale_mode="torch")
    reload_model_weights(model, PRETRAINED_DICT, "nat", pretrained)
    return model


@register_model
def NAT_Mini(input_shape=(224, 224, 3), num_classes=1000, activation="gelu", classifier_activation="softmax", pretrained="imagenet", **kwargs):
    num_blocks = [3, 4, 6, 5]
    return NAT(**locals(), model_name="nat_mini", **kwargs)


@register_model
def NAT_Tiny(input_shape=(224, 224, 3), num_classes=1000, activation="gelu", classifier_activation="softmax", pretrained="imagenet", **kwargs):
    num_blocks = [3, 4, 18, 5]
    return NAT(**locals(), model_name="nat_tiny", **kwargs)


@register_model
def NAT_Small(input_shape=(224, 224, 3), num_classes=1000, activation="gelu", classifier_activation="softmax", pretrained="imagenet", **kwargs):
    num_blocks = [3, 4, 18, 5]
    num_heads = [3, 6, 12, 24]
    out_channels = [96, 192, 384, 768]
    mlp_ratio = kwargs.pop("mlp_ratio", 2)
    layer_scale = kwargs.pop("layer_scale", 1e-5)
    return NAT(**locals(), model_name="nat_small", **kwargs)


@register_model
def NAT_Base(input_shape=(224, 224, 3), num_classes=1000, activation="gelu", classifier_activation="softmax", pretrained="imagenet", **kwargs):
    num_blocks = [3, 4, 18, 5]
    num_heads = [4, 8, 16, 32]
    out_channels = [128, 256, 512, 1024]
    mlp_ratio = kwargs.pop("mlp_ratio", 2)
    layer_scale = kwargs.pop("layer_scale", 1e-5)
    return NAT(**locals(), model_name="nat_base", **kwargs)
