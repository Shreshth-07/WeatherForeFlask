from flaskBlog import app
import os

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))





