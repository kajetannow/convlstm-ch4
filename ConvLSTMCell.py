import torch
import torch.nn as nn

# Original ConvLSTM cell as proposed by Shi et al.
class ConvLSTMCell(nn.Module):

    def __init__(self, in_channels, out_channels, 
    kernel_size, padding, activation, frame_size):

        super(ConvLSTMCell, self).__init__()
        self.out_channels = out_channels

        if activation == "tanh":
            self.activation = torch.tanh 
        elif activation == "relu":
            self.activation = torch.relu
        
        # Idea adapted from https://github.com/ndrplz/ConvLSTM_pytorch
        self.conv = nn.Conv2d(
            in_channels=in_channels + out_channels, 
            out_channels=4 * out_channels, 
            kernel_size=kernel_size, 
            padding=padding)           

        # Initialize weights for Hadamard Products
        self.W_ci = nn.Parameter(torch.Tensor(out_channels, *frame_size))
        nn.init.xavier_uniform_(self.W_ci)
        self.W_co = nn.Parameter(torch.Tensor(out_channels, *frame_size))
        nn.init.xavier_uniform_(self.W_co)
        self.W_cf = nn.Parameter(torch.Tensor(out_channels, *frame_size))
        nn.init.xavier_uniform_(self.W_cf)


    def forward(self, X, H_prev, C_prev):

        # Idea adapted from https://github.com/ndrplz/ConvLSTM_pytorch
        if torch.isnan(X).any():
            print("THERE IS NAN IN X")
        if torch.isnan(H_prev).any():
            print("THERE IS NAN IN H_prev")
        if torch.isnan(C_prev).any():
            print("THERE IS NAN IN C_prev")
        conv_output = self.conv(torch.cat([X, H_prev], dim=1))
        # print("conv_output")
        # print(conv_output.mean())

        # Idea adapted from https://github.com/ndrplz/ConvLSTM_pytorch
        i_conv, f_conv, C_conv, o_conv = torch.chunk(conv_output, chunks=4, dim=1)
        # print(i_conv.mean())
        # print(f_conv.mean())
        # print(C_conv.mean())
        # print(o_conv.mean())
        # print("self wci")
        # print(self.W_ci.mean())

        if torch.isnan(i_conv).any():
            print("THERE IS NAN IN i_conv")
        if torch.isnan(f_conv).any():
            print("THERE IS NAN IN f_conv")
        if torch.isnan(C_conv).any():
            print("THERE IS NAN IN C_conv")
        if torch.isnan(o_conv).any():
            print("THERE IS NAN IN o_conv")

        input_gate = torch.sigmoid(torch.clamp((i_conv + self.W_ci * C_prev), min=-50, max=50))
        # print("input_gate")
        # print(input_gate.mean())
        forget_gate = torch.sigmoid(f_conv + self.W_cf * C_prev )
        forget_gate = torch.clamp(forget_gate, min=-50, max=50)
        # print("forget_gate")
        # print(forget_gate.mean())


        # Current Cell output
        C = forget_gate*C_prev + input_gate * self.activation(C_conv)
        C = torch.clamp(C, min=-50, max=50)
        # print(C.mean())

        output_gate = torch.sigmoid(o_conv + self.W_co * C )
        output_gate = torch.clamp(output_gate, min=-50, max=50)

        # Current Hidden State
        H = output_gate * self.activation(C)

        return H, C