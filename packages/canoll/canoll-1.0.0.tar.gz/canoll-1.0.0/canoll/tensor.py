class Tensor:
    def __init__(self, data):
        """Inisialisasi Tensor dari list/nested list."""
        if isinstance(data[0], (list, tuple)):
            self.shape = (len(data), len(data[0]))
            self.data = [item for sublist in data for item in sublist]  # Flatten
        else:
            self.shape = (len(data),)
            self.data = list(data)
    
    def __add__(self, other):
        """Penjumlahan element-wise."""
        if self.shape != other.shape:
            raise ValueError("Shape tidak sesuai!")
        return Tensor([a + b for a, b in zip(self.data, other.data)])
    
    def __repr__(self):
        return f"Canoll.Tensor(shape={self.shape})"
