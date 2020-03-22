# covid19-iceland


Logistic curve fit for confirmed Covid-19 cases in Iceland, using Python3, scipy and matplotlib. 

Data is retrieved from [covid.is](https://www.covid.is/tolulegar-upplysingar) and maximum case assumption based on [covid.hi.is](https://covid.hi.is).

Setup
--

````bash
python3 -m venv virtualenv
. virtualenv/bin/activate
pip3 install -r requirements.txt
````

Usage
---

```bash
./logistic-curve-fit.py iceland.csv
```

Sample resulting plot
---
![image](https://user-images.githubusercontent.com/38035/77252804-40e1a500-6c4e-11ea-9e74-87ba73d098dc.png)
