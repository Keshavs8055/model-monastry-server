from flask_app import create_app
app = create_app()

@app.route('/health')
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
