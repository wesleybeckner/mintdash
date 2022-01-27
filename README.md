# MintDash
a minty dashboard!

* [The Original](https://mintdash.azurewebsites.net/) ([Medium Article](https://medium.com/@wesleybeckner/a-minty-mint-dashboard-with-plotly-dash-bbaf09ca2f6a))
* [The Jamstack Version](https://wesleybeckner.github.io/mintdash/) ([Medium Article](https://medium.com/@wesleybeckner/from-monolithic-to-jamstack-what-a-data-scientist-needs-to-know-for-modern-single-page-c6ef2f235567))

![image](assets/snap1.PNG)

```
git clone https://github.com/wesleybeckner/mintdash.git
cd mintdash
pip install -r requirements.txt
python wsgi.py
```

## Notes

If you want the configuration settings to set properly you will need to create a local `.env` file with the parameters referenced in `config.py`

For a full reference on how Flask and Dash are setup visit [Todds article](https://hackersandslackers.com/plotly-dash-with-flask/)
