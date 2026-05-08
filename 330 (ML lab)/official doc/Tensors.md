## Operations on Tensors

Over 1200 tensor operations, including arithmetic, linear algebra, matrix manipulation (transposing, indexing, slicing), sampling and more are comprehensively described [here](https://pytorch.org/docs/stable/torch.html).

Each of these operations can be run on the CPU and [Accelerator](https://pytorch.org/docs/stable/torch.html#accelerators) such as CUDA, MPS, MTIA, or XPU. If you’re using Colab, allocate an accelerator by going to Runtime > Change runtime type > GPU.

By default, tensors are created on the CPU. We need to explicitly move tensors to the accelerator using `.to` method (after checking for accelerator availability). Keep in mind that copying large tensors across devices can be expensive in terms of time and memory!

# We move our tensor to the current accelerator if available
if [torch.accelerator.is_available](https://docs.pytorch.org/docs/stable/generated/torch.accelerator.is_available.html#torch.accelerator.is_available "torch.accelerator.is_available")():
    [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").to([torch.accelerator.current_accelerator](https://docs.pytorch.org/docs/stable/generated/torch.accelerator.current_accelerator.html#torch.accelerator.current_accelerator "torch.accelerator.current_accelerator")())

Try out some of the operations from the list. If you’re familiar with the NumPy API, you’ll find the Tensor API a breeze to use.

**Standard numpy-like indexing and slicing:**

[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.ones](https://docs.pytorch.org/docs/stable/generated/torch.ones.html#torch.ones "torch.ones")(4, 4)
print(f"First row: {[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")[0]}")
print(f"First column: {[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")[:, 0]}")
print(f"Last column: {[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")[..., -1]}")
[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")[:,1] = 0
print([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

First row: tensor([1., 1., 1., 1.])
First column: tensor([1., 1., 1., 1.])
Last column: tensor([1., 1., 1., 1.])
tensor([[1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.]])

**Joining tensors** You can use `torch.cat` to concatenate a sequence of tensors along a given dimension. See also [torch.stack](https://pytorch.org/docs/stable/generated/torch.stack.html), another tensor joining operator that is subtly different from `torch.cat`.

[t1](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.cat](https://docs.pytorch.org/docs/stable/generated/torch.cat.html#torch.cat "torch.cat")([[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")], dim=1)
print([t1](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

tensor([[1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1.],
        [1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1.],
        [1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1.],
        [1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1.]])

**Arithmetic operations**

# This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
# ``tensor.T`` returns the transpose of a tensor
[y1](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") @ [tensor.T](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")
[y2](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").matmul([tensor.T](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

[y3](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.rand_like](https://docs.pytorch.org/docs/stable/generated/torch.rand_like.html#torch.rand_like "torch.rand_like")([y1](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))
[torch.matmul](https://docs.pytorch.org/docs/stable/generated/torch.matmul.html#torch.matmul "torch.matmul")([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), [tensor.T](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), out=[y3](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

# This computes the element-wise product. z1, z2, z3 will have the same value
[z1](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") * [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")
[z2](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").mul([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

[z3](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.rand_like](https://docs.pytorch.org/docs/stable/generated/torch.rand_like.html#torch.rand_like "torch.rand_like")([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))
[torch.mul](https://docs.pytorch.org/docs/stable/generated/torch.mul.html#torch.mul "torch.mul")([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"), out=[z3](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

tensor([[1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.]])

**Single-element tensors** If you have a one-element tensor, for example by aggregating all values of a tensor into one value, you can convert it to a Python numerical value using `item()`:

[agg](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").sum()
agg_item = [agg](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").item()
print(agg_item, type(agg_item))

12.0 <class 'float'>

**In-place operations** Operations that store the result into the operand are called in-place. They are denoted by a `_` suffix. For example: `x.copy_(y)`, `x.t_()`, will change `x`.

print(f"{[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")} \n")
[tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").add_(5)
print([tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor"))

tensor([[1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.],
        [1., 0., 1., 1.]])

tensor([[6., 5., 6., 6.],
        [6., 5., 6., 6.],
        [6., 5., 6., 6.],
        [6., 5., 6., 6.]])

Note

In-place operations save some memory, but can be problematic when computing derivatives because of an immediate loss of history. Hence, their use is discouraged.

---

## Bridge with NumPy

Tensors on the CPU and NumPy arrays can share their underlying memory locations, and changing one will change the other.

### Tensor to NumPy array

[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.ones](https://docs.pytorch.org/docs/stable/generated/torch.ones.html#torch.ones "torch.ones")(5)
print(f"t: {[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")}")
n = [t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").numpy()
print(f"n: {n}")

t: tensor([1., 1., 1., 1., 1.])
n: [1. 1. 1. 1. 1.]

A change in the tensor reflects in the NumPy array.

[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor").add_(1)
print(f"t: {[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")}")
print(f"n: {n}")

t: tensor([2., 2., 2., 2., 2.])
n: [2. 2. 2. 2. 2.]

### NumPy array to Tensor

n = np.ones(5)
[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor") = [torch.from_numpy](https://docs.pytorch.org/docs/stable/generated/torch.from_numpy.html#torch.from_numpy "torch.from_numpy")(n)

Changes in the NumPy array reflects in the tensor.

np.add(n, 1, out=n)
print(f"t: {[t](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "torch.Tensor")}")
print(f"n: {n}")

t: tensor([2., 2., 2., 2., 2.], dtype=torch.float64)
n: [2. 2. 2. 2. 2.]

**Total running time of the script:** (0 minutes 0.489 seconds)