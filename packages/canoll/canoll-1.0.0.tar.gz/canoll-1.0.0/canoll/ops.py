def matmul(a: Tensor, b: Tensor) -> Tensor:
    """Dot product matrix (optimasi untuk CPU)."""
    if a.shape[1] != b.shape[0]:
        raise ValueError("Dimensi tidak valid!")
    
    result = []
    for i in range(a.shape[0]):
        row = []
        for j in range(b.shape[1]):
            val = sum(a.data[i*a.shape[1] + k] * b.data[k*b.shape[1] + j] 
                      for k in range(a.shape[1]))
            row.append(val)
        result.append(row)
    return Tensor(result)
