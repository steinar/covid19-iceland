# covid19-iceland


Logistic curve fit for confirmed Covid-19 cases in Iceland, using Python3, scipy and matplotlib.

**THIS PROJECT IS PURELY FOR EXPERIMENTAL PURPOSES.** Refer to the [official model](https://covid.hi.is/) for meaningful  
information.  

Data is retrieved from [covid.is](https://www.covid.is/tolulegar-upplysingar) and maximum case assumption based on 
[covid.hi.is](https://covid.hi.is).

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
![image](https://user-images.githubusercontent.com/38035/77434757-40294a00-6dd9-11ea-9811-c6f3d52f20e3.png)
