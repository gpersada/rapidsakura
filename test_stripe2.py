import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
styler = df.style.format(precision=2).set_properties(**{'background-color': 'rgba(128, 128, 128, 0.1)'}, subset=pd.IndexSlice[::2, :])
print("Styler created successfully")
