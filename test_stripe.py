import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))

def make_pretty(styler):
    styler.set_properties(**{'background-color': 'rgba(128, 128, 128, 0.2)'}, subset=pd.IndexSlice[::2, :])
    return styler

st.dataframe(df.style.pipe(make_pretty))

