# rng_alg

# Description

This add some random algorithm with pi, hex, advanced rng and special charactere generator

## 📦 Installation 📦

Just one command

```pip
pip install rng_alg
```

## Use

```python
import rng_alg
```

### Random with pi

```python
rng_alg.RGN.pi_alg()
```

### normal avanced rng

```python
rng_alg.RGN.advanced_rng(1, 40) # generate between 1 to 40
```

### hexadecimal

```python
rng_alg.RGN.hex() # generate hexadecimal number between 1 to FFFFF

rng_alg.RGN.hex(100, 1000) # generate hexadecimal number between 100 to 1000

rng_alg.RGN.hex(None, 5000) # generate hexadecimal number between 1 to 5000

rng_alg.RGN.hex(200, None) # generate hexadecimal number between 200 to FFFFF
```

### generate special charactere

```python
rng_alg.RGN.special_char_gen() # 1 special charactere

rng_alg.RGN.special_char_gen(5) # 5 special charactere

rng_alg.RGN.special_char_gen(10) # 10 special charactere
```