# rngalg

# Description

This add some random algorithm with pi, hex, advanced rng and special charactere generator

## 📦 Installation 📦

Just one command

```pip
pip install rng-alg
```

## Use

```python
import rngalg
```

### Random with pi

```python
rngalg.pialg()
```

### normal avanced rng

```python
rngalg.advancedrng(1, 40) # generate between 1 to 40
```

### hexadecimal

```python
rngalg.hex() # generate hexadecimal number between 1 to FFFFF

rngalg.hex(100, 1000) # generate hexadecimal number between 100 to 1000

rngalg.hex(None, 5000) # generate hexadecimal number between 1 to 5000

rngalg.hex(200, None) # generate hexadecimal number between 200 to FFFFF
```

### generate special charactere

```python
rngalg.specialchargen() # 1 special charactere

rngalg.specialchargen(5) # 5 special charactere

rngalg.specialchargen(10) # 10 special charactere
```