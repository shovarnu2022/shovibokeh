from flask import Flask, render_template

app = Flask(__name__)


@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    df = data.DataReader(name="GOOG", data_source="yahoo",
                         start="3/2/2019", end="6/20/2019")

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Close-df.Open)

    p = figure(x_axis_type='datetime', width=1000,
               height=300, sizing_mode='stretch_both')
    p.title.text = "Candlestick chart"
    p.title.align = "center"
    p.title.text_font = "Verdana"
    p.grid.grid_line_alpha = 0.5

    hours_12 = 12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.status == "Increase"], df.Middle[df.status == "Increase"], hours_12,
           df.Height[df.status == "Increase"], fill_color="#CCFFFF", line_color="black")

    p.rect(df.index[df.status == "Decrease"], df.Middle[df.status == "Decrease"], hours_12,
           df.Height[df.status == "Decrease"], fill_color="#FF3333", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html",
                           script1=script1,
                           div1=div1,
                           cdn_css=cdn_css,
                           cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
