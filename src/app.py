import sys
import os

# Ensure the current working directory is first on sys.path so a config.py placed
# next to the executable can be imported when running the PyInstaller bundle.
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from flask import Flask, render_template, request, send_from_directory, redirect, send_file, make_response, session
from replication_package import rep_package_start
import pandas as pd
from utils import generate_wordcloud
from data.data_analysis import data_analysis
import os
import time
import shutil
import zipfile
import io
import tempfile
import zipfile
import io

app = Flask(__name__, static_folder='static')
app.secret_key = 'replication_package_secret_key'

@app.route('/config', methods=['GET', 'POST'])
def config_page():
    if request.method == 'POST':
        elsevier_api = request.form.get('elsevier_api', '')
        elsevier_inst = request.form.get('elsevier_inst', '')
        ieee_api = request.form.get('ieee_api', '')
        springer_api = request.form.get('springer_api', '')
        
        config_path = os.path.join(os.getcwd(), 'api_config.py')
        with open(config_path, 'w') as f:
            f.write(f"ELSEVIER_API_KEY = '{elsevier_api}'\n")
            f.write(f"ELSEVIER_INST_TOKEN = '{elsevier_inst}'\n")
            f.write(f"IEEE_API_KEY = '{ieee_api}'\n")
            f.write(f"SPRINGER_API_KEY = '{springer_api}'\n")
        
        return redirect('/dashboard')
    else:
        current = {}
        config_path = os.path.join(os.getcwd(), 'api_config.py')
        if os.path.exists(config_path):
            try:
                import sys
                sys.path.insert(0, os.getcwd())
                import api_config
                current = {
                    'elsevier_api': getattr(api_config, 'ELSEVIER_API_KEY', ''),
                    'elsevier_inst': getattr(api_config, 'ELSEVIER_INST_TOKEN', ''),
                    'ieee_api': getattr(api_config, 'IEEE_API_KEY', ''),
                    'springer_api': getattr(api_config, 'SPRINGER_API_KEY', '')
                }
            except ImportError:
                pass
        else:
            try:
                from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, IEEE_API_KEY, SPRINGER_API_KEY
                current = {
                    'elsevier_api': ELSEVIER_API_KEY,
                    'elsevier_inst': ELSEVIER_INST_TOKEN,
                    'ieee_api': IEEE_API_KEY,
                    'springer_api': SPRINGER_API_KEY
                }
            except ImportError:
                pass
        return render_template('config.html', current=current)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    # This would normally fetch and display real data
    data = {
        "title": "Dashboard",
        "content": "Welcome to the Replication Package Builder!"
    }
    available_sources = {
        'scopus': False,
        'ieee': False,
        'engineering_village': False,
        'science_direct': False,
        'hal_open_science': True,  # No API key needed
        'acm_digital_library': True,  # No API key needed
        'springer_nature': False
    }
    config_path = os.path.join(os.getcwd(), 'api_config.py')
    if os.path.exists(config_path):
        try:
            import sys
            sys.path.insert(0, os.getcwd())
            import api_config
            if getattr(api_config, 'ELSEVIER_API_KEY', '') and getattr(api_config, 'ELSEVIER_INST_TOKEN', ''):
                available_sources['scopus'] = True
                available_sources['engineering_village'] = True
                available_sources['science_direct'] = True
            if getattr(api_config, 'IEEE_API_KEY', ''):
                available_sources['ieee'] = True
            if getattr(api_config, 'SPRINGER_API_KEY', ''):
                available_sources['springer_nature'] = True
        except ImportError:
            pass
    else:
        try:
            from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN
            if ELSEVIER_API_KEY and ELSEVIER_INST_TOKEN:
                available_sources['scopus'] = True
                available_sources['engineering_village'] = True
                available_sources['science_direct'] = True
        except:
            pass
        try:
            from config import IEEE_API_KEY
            if IEEE_API_KEY:
                available_sources['ieee'] = True
        except:
            pass
        try:
            from config import SPRINGER_API_KEY
            if SPRINGER_API_KEY:
                available_sources['springer_nature'] = True
        except:
            pass
    return render_template("dashboard.html", **data, available_sources=available_sources)

@app.route("/run", methods=["POST"])
def run():
    data_flags = {
        "scopus": "scopus" in request.form,
        "ieee": "ieee" in request.form,
        "engineering_village": "engineering_village" in request.form,
        "science_direct": "science_direct" in request.form,
        "hal_open_science": "hal_open_science" in request.form,
        "acm_digital_library": "acm_digital_library" in request.form,
        "springer_nature": "springer_nature" in request.form,
    }
    selected_terms = []
    categories_terms = {}
    terms_keys = [k for k in request.form.keys() if k.startswith('custom_terms')]
    for key in sorted(terms_keys, key=lambda x: int(x.split('custom_terms')[1])):
        cat_key = key.replace('custom_terms', 'custom_category')
        category = request.form.get(cat_key, '')
        terms_str = request.form[key]
        if terms_str:
            terms = [t.strip() for t in terms_str.split(',') if t.strip()]
            selected_terms.extend(terms)
            categories_terms[category] = terms
    if selected_terms:
        custom_query = ' AND '.join(f'"{term}"' for term in selected_terms)
    else:
        custom_query = ''
    queries = {
        "scopus": custom_query,
        "ieee": custom_query,
        "engineering_village": custom_query,
        "science_direct": custom_query,
        "hal_open_science": custom_query,
        "acm_digital_library": custom_query,
        "springer_nature": custom_query,
    }
    session['categories_terms'] = categories_terms
    try:
        # Start the replication package build
        results = rep_package_start(data_flags, queries)
        
        # Generate wordcloud for venues
        all_data = []
        for source, items in results.items():
            for item in items:
                item_copy = item.copy()
                item_copy['Source'] = source.replace('_', ' ').title()
                all_data.append(item_copy)
        if all_data:
            df = pd.DataFrame(all_data)
            if 'Venue' in df.columns:
                value_counts = df['Venue'].value_counts()
                image_path = generate_wordcloud(value_counts.to_dict())
                # Move to generated_images
                generated_dir = os.path.join(os.getcwd(), 'generated_images')
                os.makedirs(generated_dir, exist_ok=True)
                shutil.move(image_path, os.path.join(generated_dir, 'venue_wordcloud.png'))
            
            # Perform data analysis
            data_analysis(df, output_dir=os.path.join(os.getcwd(), 'generated_images'))
        
        return render_template("results.html", title="Replication Results", message="Replication package build completed.", results=results, timestamp=int(time.time()), query=custom_query)
    except Exception as e:
        return render_template("error.html", error_code=500, error_message=str(e)), 500

@app.route('/data_results/<filename>')
def serve_file(filename):
    return send_from_directory('data_results', filename)

@app.route('/generated_images/<filename>')
def serve_generated_image(filename):
    generated_dir = os.path.join(os.getcwd(), 'generated_images')
    return send_from_directory(generated_dir, filename)

@app.route('/export_query')
def export_query():
    categories_terms = session.get('categories_terms', {})
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Category', 'Term'])
    for category, terms in categories_terms.items():
        if category:  # Skip empty categories
            for term in terms:
                writer.writerow([category, term])
    content = output.getvalue()
    output.close()
    response = make_response(content)
    response.headers['Content-Disposition'] = 'attachment; filename=query_terms.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/download_images')
def download_images():
    images = [
        'venue_wordcloud.png',
        'publication_year_distribution.png',
        'publication_venue_distribution.png',
        'publication_venue_type_distribution.png',
        'publication_source_distribution.png',
        'publication_authors_distribution.png'
    ]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        generated_dir = os.path.join(os.getcwd(), 'generated_images')
        for img in images:
            img_path = os.path.join(generated_dir, img)
            if os.path.exists(img_path):
                zip_file.write(img_path, img)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='charts.zip')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == "__main__":
    app.run()