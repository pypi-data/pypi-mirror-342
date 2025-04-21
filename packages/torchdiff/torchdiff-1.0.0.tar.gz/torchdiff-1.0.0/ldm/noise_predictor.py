import torch
import torch.nn as nn



class NoisePredictor(nn.Module):
    """U-Net-like architecture for noise prediction in Latent Diffusion Models.

    Predicts noise in the latent space for diffusion models (DDPM, DDIM, SDE), incorporating
    time embeddings and optional text conditioning. Used as the `noise_predictor` in
    `TrainLDM` and `SampleLDM` from the `ldm` module.

    Parameters
    ----------
    in_channels : int
        Number of input channels (matches latent channels from `AutoencoderLDM`).
    down_channels : list of int
        List of output channels for downsampling blocks.
    mid_channels : list of int
        List of channels for middle blocks.
    up_channels : list of int
        List of output channels for upsampling blocks.
    down_sampling : list of bool
        List indicating whether to downsample in each down block.
    time_embed_dim : int
        Dimensionality of time embeddings.
    y_embed_dim : int
        Dimensionality of text embeddings for conditioning.
    num_down_blocks : int
        Number of convolutional layer pairs per down block.
    num_mid_blocks : int
        Number of convolutional layer pairs per middle block.
    num_up_blocks : int
        Number of convolutional layer pairs per up block.
    dropout_rate : float, optional
        Dropout rate for convolutional and attention layers (default: 0.1).
    down_sampling_factor : int, optional
        Factor for spatial downsampling/upsampling (default: 2).
    where_y : bool, optional
        If True, text embeddings are used in attention; if False, concatenated to input
        (default: True).
    y_to_all : bool, optional
        If True, apply text-conditioned attention to all layers; if False, only first layer
        (default: False).

    Attributes
    ----------
    in_channels : int
        Number of input channels.
    down_channels : list of int
        Channels for downsampling blocks.
    mid_channels : list of int
        Channels for middle blocks.
    up_channels : list of int
        Channels for upsampling blocks.
    down_sampling : list of bool
        Downsampling flags.
    time_embed_dim : int
        Time embedding dimension.
    y_embed_dim : int
        Text embedding dimension.
    num_down_blocks : int
        Number of layer pairs per down block.
    num_mid_blocks : int
        Number of layer pairs per middle block.
    num_up_blocks : int
        Number of layer pairs per up block.
    dropout_rate : float
        Dropout rate.
    where_y : bool
        Flag for text embedding usage.
    up_sampling : list of bool
        Reversed `down_sampling` for upsampling blocks.
    conv1 : torch.nn.Conv2d
        Initial 3x3 convolutional layer.
    time_projection : torch.nn.Sequential
        Projection for time embeddings.
    down_blocks : torch.nn.ModuleList
        List of DownBlock modules for downsampling.
    mid_blocks : torch.nn.ModuleList
        List of MiddleBlock modules for bottleneck processing.
    up_blocks : torch.nn.ModuleList
        List of UpBlock modules for upsampling.
    conv2 : torch.nn.Sequential
        Final convolutional layer with group normalization and dropout.

    Notes
    -----
    - The architecture follows a U-Net structure with downsampling, bottleneck, and
      upsampling blocks, incorporating time embeddings and optional text conditioning via
      attention or concatenation.
    - Skip connections link down and up blocks, with channel adjustments for concatenation.
    - Weights are initialized with Kaiming normal (Leaky ReLU nonlinearity) for stability.
    - Input and output tensors have the same shape, matching the latent space of
      `AutoencoderLDM`.
    """
    def __init__(
            self,
            in_channels,
            down_channels,
            mid_channels,
            up_channels,
            down_sampling,
            time_embed_dim,
            y_embed_dim, # output embedding dimension in text conditional net
            num_down_blocks,
            num_mid_blocks,
            num_up_blocks,
            dropout_rate=0.1,
            down_sampling_factor=2,
            where_y=True,
            y_to_all=False
    ):
        super().__init__()
        self.in_channels = in_channels
        self.down_channels = down_channels
        self.mid_channels = mid_channels
        self.up_channels = up_channels
        self.down_sampling = down_sampling
        self.time_embed_dim = time_embed_dim
        self.y_embed_dim = y_embed_dim
        self.num_down_blocks = num_down_blocks
        self.num_mid_blocks = num_mid_blocks
        self.num_up_blocks = num_up_blocks
        self.dropout_rate = dropout_rate
        self.where_y = where_y
        self.up_sampling = list(reversed(self.down_sampling))
        self.conv1 = nn.Conv2d(
            in_channels=self.in_channels,
            out_channels=self.down_channels[0],
            kernel_size=3,
            padding=1
        )
        # initial time embedding projection
        self.time_projection = nn.Sequential(
            nn.Linear(in_features=self.time_embed_dim, out_features=self.time_embed_dim),
            nn.SiLU(),
            nn.Linear(in_features=self.time_embed_dim, out_features=self.time_embed_dim)
        )
        # down blocks
        self.down_blocks = nn.ModuleList([
            DownBlock(
                in_channels=self.down_channels[i],
                out_channels=self.down_channels[i+1],
                time_embed_dim=self.time_embed_dim,
                y_embed_dim=y_embed_dim,
                num_layers=self.num_down_blocks,
                down_sampling_factor=down_sampling_factor,
                down_sample=self.down_sampling[i],
                dropout_rate=self.dropout_rate,
                y_to_all=y_to_all
            ) for i in range(len(self.down_channels)-1)
        ])
        # middle blocks
        self.mid_blocks = nn.ModuleList([
            MiddleBlock(
                in_channels=self.mid_channels[i],
                out_channels=self.mid_channels[i + 1],
                time_embed_dim=self.time_embed_dim,
                y_embed_dim=y_embed_dim,
                num_layers=self.num_mid_blocks,
                dropout_rate=self.dropout_rate,
                y_to_all=y_to_all
            ) for i in range(len(self.mid_channels) - 1)
        ])
        # up blocks
        skip_channels = list(reversed(self.down_channels))
        self.up_blocks = nn.ModuleList([
            UpBlock(
                in_channels=self.up_channels[i],
                out_channels=self.up_channels[i+1],
                skip_channels=skip_channels[i],
                time_embed_dim=self.time_embed_dim,
                y_embed_dim=y_embed_dim,
                num_layers=self.num_up_blocks,
                up_sampling_factor=down_sampling_factor,
                up_sampling=self.up_sampling[i],
                dropout_rate=self.dropout_rate,
                y_to_all=y_to_all
            ) for i in range(len(self.up_channels)-1)
        ])
        # final convolution layer
        self.conv2 = nn.Sequential(
            nn.GroupNorm(num_groups=8, num_channels=self.up_channels[-1]),
            nn.Dropout(p=self.dropout_rate),
            nn.Conv2d(in_channels=self.up_channels[-1], out_channels=self.in_channels, kernel_size=3, padding=1)
        )

    def initialize_weights(self):
        """Initializes model weights for training stability.

        Applies Kaiming normal initialization to convolutional and linear layers with
        Leaky ReLU nonlinearity (a=0.2), and zeros biases.
        """
        for module in self.modules():
            if isinstance(module, (nn.Conv2d, nn.Linear, nn.ConvTranspose2d)):
                nn.init.kaiming_normal_(module.weight, a=0.2, nonlinearity='leaky_relu')
                if module.bias is not None:
                    nn.init.zeros_(module.bias)

    def forward(self, x, t, y=None):
        """Predicts noise given latent input, time step, and optional text conditioning.

        Parameters
        ----------
        x : torch.Tensor
            Input latent tensor, shape (batch_size, in_channels, height, width).
        t : torch.Tensor
            Time steps, shape (batch_size,).
        y : torch.Tensor, optional
            Text embeddings for conditioning, shape (batch_size, seq_len, y_embed_dim)
            or (batch_size, y_embed_dim) (default: None).

        Returns
        -------
        torch.Tensor
            Predicted noise, same shape as input `x`.
        """
        if not self.where_y and y is not None:
            x = torch.cat(tensors=[x, y], dim=1)
        output = self.conv1(x)
        time_embed = GetEmbeddedTime(embed_dim=self.time_embed_dim)(time_steps=t)
        time_embed = self.time_projection(time_embed)
        skip_connections = []

        for i, down in enumerate(self.down_blocks):
            skip_connections.append(output)
            output = down(x=output, embed_time=time_embed, y=y)
        for i, mid in enumerate(self.mid_blocks):
            output = mid(x=output, embed_time=time_embed, y=y)
        for i, up in enumerate(self.up_blocks):
            skip_connection = skip_connections.pop()
            output = up(x=output, skip_connection=skip_connection, embed_time=time_embed, y=y)

        output = self.conv2(output)
        return output
#-----------------------------------------------------------------------------
class DownBlock(nn.Module):
    """Downsampling block for NoisePredictor’s encoder.

    Applies convolutional layers with residual connections, time embeddings, and optional
    text-conditioned attention, followed by downsampling if enabled.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    time_embed_dim : int
        Dimensionality of time embeddings.
    y_embed_dim : int
        Dimensionality of text embeddings.
    num_layers : int
        Number of convolutional layer pairs (Conv3).
    down_sampling_factor : int
        Factor for spatial downsampling.
    down_sample : bool
        If True, apply downsampling; if False, use identity (no downsampling).
    dropout_rate : float
        Dropout rate for Conv3 and attention layers.
    y_to_all : bool
        If True, apply text-conditioned attention to all layers; if False, only first layer.

    Attributes
    ----------
    num_layers : int
        Number of convolutional layer pairs.
    y_to_all : bool
        Flag for text-conditioned attention scope.
    conv1 : torch.nn.ModuleList
        List of Conv3 layers for first convolution in each pair.
    conv2 : torch.nn.ModuleList
        List of Conv3 layers for second convolution in each pair.
    time_embedding : torch.nn.ModuleList
        List of TimeEmbedding modules for time conditioning.
    attention : torch.nn.ModuleList
        List of Attention modules for text conditioning or self-attention.
    down_sampling : DownSampling or torch.nn.Identity
        Downsampling module or identity if `down_sample=False`.
    resnet : torch.nn.ModuleList
        List of 1x1 convolutional layers for residual connections.
    """
    def __init__(self, in_channels, out_channels, time_embed_dim, y_embed_dim,num_layers, down_sampling_factor,  down_sample, dropout_rate, y_to_all):
        super().__init__()
        self.num_layers = num_layers
        self.y_to_all = y_to_all
        self.conv1 = nn.ModuleList([
            Conv3(
                in_channels=in_channels if i==0 else out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for i in range(self.num_layers)
        ])
        self.conv2 = nn.ModuleList([
            Conv3(
                in_channels=out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers)
        ])
        self.time_embedding = nn.ModuleList([
            TimeEmbedding(
                output_dim=out_channels,
                embed_dim=time_embed_dim
            ) for _ in range(self.num_layers)
        ])
        self.attention = nn.ModuleList([
            Attention(
                in_channels=out_channels,
                y_embed_dim= y_embed_dim,
                num_groups=8,
                num_heads=4,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers)
        ])
        self.down_sampling = DownSampling(
            in_channels=out_channels,
            out_channels=out_channels,
            down_sampling_factor=down_sampling_factor,
            conv_block=True,
            max_pool=True
        ) if down_sample else nn.Identity()
        self.resnet = nn.ModuleList([
            nn.Conv2d(
                in_channels=in_channels if i == 0 else out_channels,
                out_channels=out_channels,
                kernel_size=1
            ) for i in range(num_layers)

        ])

    def forward(self, x, embed_time, y):
        """Processes input through convolutions, time embeddings, attention, and downsampling.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).
        embed_time : torch.Tensor
            Time embeddings, shape (batch_size, time_embed_dim).
        y : torch.Tensor, optional
            Text embeddings, shape (batch_size, seq_len, y_embed_dim) or
            (batch_size, y_embed_dim) (default: None).

        Returns
        -------
        torch.Tensor
            Output tensor, shape (batch_size, out_channels,
            height/down_sampling_factor, width/down_sampling_factor) if downsampling;
            otherwise, same height/width as input.
        """
        output = x
        for i in range(self.num_layers):
            resnet_input = output
            output = self.conv1[i](output)
            output = output + self.time_embedding[i](embed_time)[:, :, None, None]
            output = self.conv2[i](output)
            output = output + self.resnet[i](resnet_input)
            if y is not None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is not None and self.y_to_all:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is None and self.y_to_all:
                out_attn = self.attention[i](output)
                output = output + out_attn
            elif y is None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output)
                output = output + out_attn

        output = self.down_sampling(output)
        return output
#------------------------------------------------------------------------------
class MiddleBlock(nn.Module):
    """Bottleneck block for NoisePredictor’s middle layers.

    Applies convolutional layers with residual connections, time embeddings, and optional
    text-conditioned attention, preserving spatial dimensions.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    time_embed_dim : int
        Dimensionality of time embeddings.
    y_embed_dim : int
        Dimensionality of text embeddings.
    num_layers : int
        Number of convolutional layer pairs (Conv3).
    dropout_rate : float
        Dropout rate for Conv3 and attention layers.
    y_to_all : bool, optional
        If True, apply text-conditioned attention to all layers; if False, only first layer
        (default: False).

    Attributes
    ----------
    num_layers : int
        Number of convolutional layer pairs.
    y_to_all : bool
        Flag for text-conditioned attention scope.
    conv1 : torch.nn.ModuleList
        List of Conv3 layers for first convolution in each pair.
    conv2 : torch.nn.ModuleList
        List of Conv3 layers for second convolution in each pair.
    time_embedding : torch.nn.ModuleList
        List of TimeEmbedding modules for time conditioning.
    attention : torch.nn.ModuleList
        List of Attention modules for text conditioning or self-attention.
    resnet : torch.nn.ModuleList
        List of 1x1 convolutional layers for residual connections.
    """
    def __init__(self, in_channels, out_channels, time_embed_dim,  y_embed_dim, num_layers, dropout_rate, y_to_all=False):
        super().__init__()
        self.num_layers = num_layers
        self.y_to_all = y_to_all
        self.conv1 = nn.ModuleList([
            Conv3(
                in_channels=in_channels if i == 0 else out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for i in range(self.num_layers+1)
        ])
        self.conv2 = nn.ModuleList([
            Conv3(
                in_channels=out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers+1)
        ])
        self.time_embedding = nn.ModuleList([
            TimeEmbedding(
                output_dim=out_channels,
                embed_dim=time_embed_dim
            ) for _ in range(self.num_layers+1)
        ])
        self.attention = nn.ModuleList([
            Attention(
                in_channels=out_channels,
                y_embed_dim=y_embed_dim,
                num_groups=8,
                num_heads=4,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers + 1)
        ])
        self.resnet = nn.ModuleList([
            nn.Conv2d(
                in_channels=in_channels if i == 0 else out_channels,
                out_channels=out_channels,
                kernel_size=1
            ) for i in range(num_layers+1)
        ])

    def forward(self, x, embed_time, y=None):
        """Processes input through convolutions, time embeddings, and attention.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).
        embed_time : torch.Tensor
            Time embeddings, shape (batch_size, time_embed_dim).
        y : torch.Tensor, optional
            Text embeddings, shape (batch_size, seq_len, y_embed_dim) or
            (batch_size, y_embed_dim) (default: None).

        Returns
        -------
        torch.Tensor
            Output tensor, shape (batch_size, out_channels, height, width).
        """
        output = x
        resnet_input = output
        output = self.conv1[0](output)
        output = output + self.time_embedding[0](embed_time)[:, :, None, None]
        output = self.conv2[0](output)
        output = output + self.resnet[0](resnet_input)
        for i in range(self.num_layers):
            if y is not None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is not None and self.y_to_all:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is None and self.y_to_all:
                out_attn = self.attention[i](output)
                output = output + out_attn
            elif y is None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output)
                output = output + out_attn
            resnet_input = output
            output = self.conv1[i + 1](output)
            output = output + self.time_embedding[i + 1](embed_time)[:, :, None, None]
            output = self.conv2[i + 1](output)
            output = output + self.resnet[i+1](resnet_input)
        return output
#------------------------------------------------------------------------------
class UpBlock(nn.Module):
    """Upsampling block for NoisePredictor’s decoder.

    Applies upsampling (if enabled), concatenates skip connections, and processes through
    convolutional layers with residual connections, time embeddings, and optional
    text-conditioned attention.

    Parameters
    ----------
    in_channels : int
        Number of input channels (before upsampling).
    out_channels : int
        Number of output channels.
    skip_channels : int
        Number of channels from skip connection.
    time_embed_dim : int
        Dimensionality of time embeddings.
    y_embed_dim : int
        Dimensionality of text embeddings.
    num_layers : int
        Number of convolutional layer pairs (Conv3).
    up_sampling_factor : int
        Factor for spatial upsampling.
    up_sampling : bool
        If True, apply upsampling; if False, use identity (no upsampling).
    dropout_rate : float
        Dropout rate for Conv3 and attention layers.
    y_to_all : bool, optional
        If True, apply text-conditioned attention to all layers; if False, only first layer
        (default: False).

    Attributes
    ----------
    num_layers : int
        Number of convolutional layer pairs.
    y_to_all : bool
        Flag for text-conditioned attention scope.
    conv1 : torch.nn.ModuleList
        List of Conv3 layers for first convolution in each pair.
    conv2 : torch.nn.ModuleList
        List of Conv3 layers for second convolution in each pair.
    time_embedding : torch.nn.ModuleList
        List of TimeEmbedding modules for time conditioning.
    attention : torch.nn.ModuleList
        List of Attention modules for text conditioning or self-attention.
    up_sampling : UpSampling or torch.nn.Identity
        Upsampling module or identity if `up_sampling=False`.
    resnet : torch.nn.ModuleList
        List of 1x1 convolutional layers for residual connections.
    """
    def __init__(self, in_channels, out_channels, skip_channels, time_embed_dim,  y_embed_dim, num_layers, up_sampling_factor, up_sampling=True, dropout_rate=0.2, y_to_all=False):
        super().__init__()
        self.num_layers = num_layers
        self.y_to_all = y_to_all
        effective_in_channels = in_channels//2 + skip_channels
        self.conv1 = nn.ModuleList([
            Conv3(
                in_channels=effective_in_channels  if i == 0 else out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for i in range(self.num_layers)
        ])
        self.conv2 = nn.ModuleList([
            Conv3(
                in_channels=out_channels,
                out_channels=out_channels,
                num_groups=8,
                kernel_size=3,
                norm=True,
                activation=True,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers)
        ])
        self.time_embedding = nn.ModuleList([
            TimeEmbedding(
                output_dim=out_channels,
                embed_dim=time_embed_dim
            ) for _ in range(self.num_layers)
        ])
        self.attention = nn.ModuleList([
            Attention(
                in_channels=out_channels,
                y_embed_dim=y_embed_dim,
                num_groups=8,
                num_heads=4,
                dropout_rate=dropout_rate
            ) for _ in range(self.num_layers)
        ])
        self.up_sampling = UpSampling(
            in_channels=in_channels,
            out_channels=in_channels,
            up_sampling_factor=up_sampling_factor,
            conv_block=True,
            up_sampling=True
        ) if up_sampling else nn.Identity()
        self.resnet = nn.ModuleList([
            nn.Conv2d(
                in_channels=effective_in_channels  if i == 0 else out_channels,
                out_channels=out_channels,
                kernel_size=1
            ) for i in range(num_layers)

        ])

    def forward(self, x, skip_connection, embed_time, y=None):
        """Processes input through upsampling, skip connection, convolutions, time embeddings, and attention.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).
        skip_connection : torch.Tensor
            Skip connection tensor, shape (batch_size, skip_channels,
            height*up_sampling_factor, width*up_sampling_factor).
        embed_time : torch.Tensor
            Time embeddings, shape (batch_size, time_embed_dim).
        y : torch.Tensor, optional
            Text embeddings, shape (batch_size, seq_len, y_embed_dim) or
            (batch_size, y_embed_dim) (default: None).

        Returns
        -------
        torch.Tensor
            Output tensor, shape (batch_size, out_channels,
            height*up_sampling_factor, width*up_sampling_factor) if upsampling;
            otherwise, same height/width as input (after skip connection).
        """
        x = self.up_sampling(x)
        x = torch.cat(tensors=[x, skip_connection], dim=1)
        output = x
        for i in range(self.num_layers):
            resnet_input = output
            output = self.conv1[i](output)
            output = output + self.time_embedding[i](embed_time)[:, :, None, None]
            output = self.conv2[i](output)
            output = output + self.resnet[i](resnet_input)
            if y is not None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is not None and self.y_to_all:
                out_attn = self.attention[i](output, y)
                output = output + out_attn
            elif y is None and self.y_to_all:
                out_attn = self.attention[i](output)
                output = output + out_attn
            elif y is None and not self.y_to_all and i == 0:
                out_attn = self.attention[i](output)
                output = output + out_attn
        #print("up-block output shape:", output.size())
        return output
#------------------------------------------------------------------------
class Conv3(nn.Module):
    """Convolutional layer with optional group normalization, SiLU activation, and dropout.

    Used in DownBlock, MiddleBlock, and UpBlock for feature extraction in NoisePredictor.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    num_groups : int, optional
        Number of groups for group normalization (default: 8).
    kernel_size : int, optional
        Convolutional kernel size (default: 3).
    norm : bool, optional
        If True, apply group normalization (default: True).
    activation : bool, optional
        If True, apply SiLU activation (default: True).
    dropout_rate : float, optional
        Dropout rate (default: 0.2).

    Attributes
    ----------
    conv : torch.nn.Conv2d
        Convolutional layer with specified kernel size and padding.
    group_norm : torch.nn.GroupNorm or torch.nn.Identity
        Group normalization or identity if `norm=False`.
    activation : torch.nn.SiLU or torch.nn.Identity
        SiLU activation or identity if `activation=False`.
    dropout : torch.nn.Dropout
        Dropout layer.
    """
    def __init__(self, in_channels, out_channels, num_groups=8, kernel_size=3, norm=True, activation=True, dropout_rate=0.2):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=(kernel_size - 1) // 2)
        self.group_norm = nn.GroupNorm(num_groups=num_groups, num_channels=out_channels) if norm else nn.Identity()
        self.activation = nn.SiLU() if activation else nn.Identity()
        self.dropout = nn.Dropout(p=dropout_rate)

    def forward(self, batch):
        """Processes input through convolution, normalization, activation, and dropout.

        Parameters
        ----------
        batch : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).

        Returns
        -------
        torch.Tensor
            Output tensor, shape (batch_size, out_channels, height, width).
        """
        batch = self.conv(batch)
        batch = self.group_norm(batch)
        batch = self.activation(batch)
        batch = self.dropout(batch)
        return batch
#----------------------------------------------------------------
class TimeEmbedding(nn.Module):
    """Time embedding projection for conditioning NoisePredictor layers.

    Projects time embeddings to match the channel dimension of convolutional outputs.

    Parameters
    ----------
    output_dim : int
        Output channel dimension (matches convolutional channels).
    embed_dim : int
        Input time embedding dimension.

    Attributes
    ----------
    embedding : torch.nn.Sequential
        Sequential layer with SiLU activation and linear projection.
    """
    def __init__(self, output_dim, embed_dim):
        super().__init__()
        self.embedding = nn.Sequential(
            nn.SiLU(),
            nn.Linear(in_features=embed_dim, out_features=output_dim)
        )
    def forward(self, batch):
        """Projects time embeddings to output dimension.

        Parameters
        ----------
        batch : torch.Tensor
            Time embeddings, shape (batch_size, embed_dim).

        Returns
        -------
        torch.Tensor
            Projected embeddings, shape (batch_size, output_dim).
        """
        return self.embedding(batch)
#----------------------------------------------------------------
class GetEmbeddedTime(nn.Module):
    """Generates sinusoidal time embeddings for NoisePredictor.

    Creates positional encodings for time steps using sine and cosine functions, following
    the transformer embedding approach.

    Parameters
    ----------
    embed_dim : int
        Dimensionality of the time embeddings (must be even).

    Attributes
    ----------
    embed_dim : int
        Time embedding dimension.

    Raises
    ------
    AssertionError
        If `embed_dim` is not divisible by 2.
    """
    def __init__(self, embed_dim):
        super().__init__()
        assert embed_dim % 2 == 0, "The embedding dimension must be divisible by two"
        self.embed_dim = embed_dim

    def forward(self, time_steps):
        """Generates sinusoidal embeddings for time steps.

        Parameters
        ----------
        time_steps : torch.Tensor
            Time steps, shape (batch_size,).

        Returns
        -------
        torch.Tensor
            Sinusoidal embeddings, shape (batch_size, embed_dim).
        """
        i = torch.arange(start=0, end=self.embed_dim // 2, dtype=torch.float32, device=time_steps.device)
        factor = 10000 ** (2 * i / self.embed_dim)
        embed_time = time_steps[:, None] / factor
        embed_time = torch.cat(tensors=[torch.sin(embed_time), torch.cos(embed_time)], dim=-1)
        return embed_time
#----------------------------------------------------------------
class Attention(nn.Module):
    """Attention module for NoisePredictor, supporting text conditioning or self-attention.

    Applies multi-head attention to enhance features, with optional text embeddings for
    conditional generation.

    Parameters
    ----------
    in_channels : int
        Number of input channels (embedding dimension for attention).
    y_embed_dim : int, optional
        Dimensionality of text embeddings (default: 768).
    num_heads : int, optional
        Number of attention heads (default: 4).
    num_groups : int, optional
        Number of groups for group normalization (default: 8).
    dropout_rate : float, optional
        Dropout rate for attention and output (default: 0.1).

    Attributes
    ----------
    in_channels : int
        Input channel dimension.
    y_embed_dim : int
        Text embedding dimension.
    num_heads : int
        Number of attention heads.
    dropout_rate : float
        Dropout rate.
    attention : torch.nn.MultiheadAttention
        Multi-head attention with `batch_first=True`.
    norm : torch.nn.GroupNorm
        Group normalization before attention.
    dropout : torch.nn.Dropout
        Dropout layer for output.
    y_projection : torch.nn.Linear
        Projection for text embeddings to match `in_channels`.

    Raises
    ------
    AssertionError
        If input channels do not match `in_channels`.
    ValueError
        If text embeddings (`y`) have incorrect dimensions after projection.
    """
    def __init__(self, in_channels, y_embed_dim=768, num_heads=4, num_groups=8, dropout_rate=0.1):
        super().__init__()
        self.in_channels = in_channels
        self.y_embed_dim = y_embed_dim
        self.num_heads = num_heads
        self.dropout_rate = dropout_rate
        self.attention = nn.MultiheadAttention(embed_dim=in_channels, num_heads=num_heads, dropout=dropout_rate, batch_first=True)
        self.norm = nn.GroupNorm(num_groups=num_groups, num_channels=in_channels)
        self.dropout = nn.Dropout(dropout_rate)
        self.y_projection = nn.Linear(y_embed_dim, in_channels)

    def forward(self, x, y=None):
        """Applies attention to input features with optional text conditioning.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).
        y : torch.Tensor, optional
            Text embeddings, shape (batch_size, seq_len, y_embed_dim) or
            (batch_size, y_embed_dim) (default: None).

        Returns
        -------
        torch.Tensor
            Output tensor, same shape as input `x`.
        """
        batch_size, channels, h, w = x.shape
        assert channels == self.in_channels, f"Expected {self.in_channels} channels, got {channels}"
        x_reshaped = x.view(batch_size, channels, h * w).permute(0, 2, 1)
        if y is not None:
            y = self.y_projection(y)
            if y.dim() != 3:
                if y.dim() == 2:
                    y = y.unsqueeze(1)
                else:
                    raise ValueError(
                        f"Expected y to be 2D or 3D after projection, got {y.dim()}D with shape {y.shape}"
                    )
            if y.shape[-1] != self.in_channels:
                raise ValueError(
                    f"Expected y's embedding dim to match in_channels ({self.in_channels}), got {y.shape[-1]}"
                )
            out, _ = self.attention(x_reshaped, y, y)
        else:
            out, _ = self.attention(x_reshaped, x_reshaped, x_reshaped)
        out = out.permute(0, 2, 1).view(batch_size, channels, h, w)
        out = self.norm(out)
        out = self.dropout(out)
        return out
#-----------------------------------------------------------------
class DownSampling(nn.Module):
    """Downsampling module for NoisePredictor’s DownBlock.

    Combines convolutional downsampling and max pooling (if enabled), concatenating
    outputs to preserve feature information.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    down_sampling_factor : int
        Factor for spatial downsampling.
    conv_block : bool, optional
        If True, include convolutional path (default: True).
    max_pool : bool, optional
        If True, include max pooling path (default: True).

    Attributes
    ----------
    conv_block : bool
        Flag for convolutional path.
    max_pool : bool
        Flag for max pooling path.
    down_sampling_factor : int
        Downsampling factor.
    conv : torch.nn.Sequential or torch.nn.Identity
        Convolutional path or identity if `conv_block=False`.
    pool : torch.nn.Sequential or torch.nn.Identity
        Max pooling path or identity if `max_pool=False`.
    """
    def __init__(self, in_channels, out_channels, down_sampling_factor, conv_block=True, max_pool=True):
        super().__init__()
        self.conv_block = conv_block
        self.max_pool = max_pool
        self.down_sampling_factor = down_sampling_factor
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=1),
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels // 2 if max_pool else out_channels,
                      kernel_size=3, stride=down_sampling_factor, padding=1)
        ) if conv_block else nn.Identity()
        self.pool = nn.Sequential(
            nn.MaxPool2d(kernel_size=down_sampling_factor, stride=down_sampling_factor),
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels//2 if conv_block else out_channels,
                      kernel_size=1, stride=1, padding=0)
        ) if max_pool else nn.Identity()

    def forward(self, batch):
        """Downsamples input using convolutional and/or pooling paths.

        Parameters
        ----------
        batch : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).

        Returns
        -------
        torch.Tensor
            Downsampled tensor, shape (batch_size, out_channels,
            height/down_sampling_factor, width/down_sampling_factor).
        """
        if not self.conv_block:
            return self.pool(batch)
        if not self.max_pool:
            return self.conv(batch)
        return torch.cat(tensors=[self.conv(batch), self.pool(batch)], dim=1)
#--------------------------------------------------------------------------
class UpSampling(nn.Module):
    """Upsampling module for NoisePredictor’s UpBlock.

    Combines transposed convolution and nearest-neighbor upsampling (if enabled),
    concatenating outputs to preserve feature information, with interpolation to align
    spatial dimensions if needed.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    up_sampling_factor : int
        Factor for spatial upsampling.
    conv_block : bool, optional
        If True, include transposed convolutional path (default: True).
    up_sampling : bool, optional
        If True, include nearest-neighbor upsampling path (default: True).

    Attributes
    ----------
    conv_block : bool
        Flag for convolutional path.
    up_sampling : bool
        Flag for upsampling path.
    up_sampling_factor : int
        Upsampling factor.
    conv : torch.nn.Sequential or torch.nn.Identity
        Transposed convolutional path or identity if `conv_block=False`.
    up_sample : torch.nn.Sequential or torch.nn.Identity
        Nearest-neighbor upsampling path or identity if `up_sampling=False`.
    """
    def __init__(self, in_channels, out_channels, up_sampling_factor, conv_block=True, up_sampling=True):
        super().__init__()
        self.conv_block = conv_block
        self.up_sampling = up_sampling
        self.up_sampling_factor = up_sampling_factor
        half_out_channels = out_channels // 2
        self.conv = nn.Sequential(
            nn.ConvTranspose2d(
                in_channels=in_channels,
                out_channels=half_out_channels if up_sampling else out_channels,
                kernel_size=3,
                stride=up_sampling_factor,
                padding=1,
                output_padding=up_sampling_factor - 1
            ),
            nn.Conv2d(
                in_channels=half_out_channels if up_sampling else out_channels,
                out_channels=half_out_channels if up_sampling else out_channels,
                kernel_size=1,
                stride=1,
                padding=0
            )
        ) if conv_block else nn.Identity()

        self.up_sample = nn.Sequential(
            nn.Upsample(scale_factor=up_sampling_factor, mode="nearest"),
            nn.Conv2d(in_channels=in_channels, out_channels=half_out_channels if conv_block else out_channels,
                      kernel_size=1, stride=1, padding=0)
        ) if up_sampling else nn.Identity()

    def forward(self, batch):
        """Upsamples input using convolutional and/or upsampling paths.

        Parameters
        ----------
        batch : torch.Tensor
            Input tensor, shape (batch_size, in_channels, height, width).

        Returns
        -------
        torch.Tensor
            Upsampled tensor, shape (batch_size, out_channels,
            height*up_sampling_factor, width*up_sampling_factor).

        Notes
        -----
        - Interpolation is applied if the spatial dimensions of the convolutional and
          upsampling paths differ, using nearest-neighbor mode.
        """
        if not self.conv_block:
            return self.up_sample(batch)
        if not self.up_sampling:
            return self.conv(batch)
        conv_output = self.conv(batch)
        up_sample_output = self.up_sample(batch)
        if conv_output.shape[2:] != up_sample_output.shape[2:]:
            _, _, h, w = conv_output.shape
            up_sample_output = torch.nn.functional.interpolate(
                up_sample_output,
                size=(h, w),
                mode='nearest'
            )
        return torch.cat(tensors=[conv_output, up_sample_output], dim=1)