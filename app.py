from flask import Flask, render_template, request, send_file, url_for,  make_response
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
import io
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

@app.after_request
def add_cache_control(response):
    # Set cache control headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_heatmap/<filename>')
def download_heatmap(filename):
    return send_file(filename, as_attachment=True)

@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    # CSV-Daten aus dem Request-Formular lesen
    csv_file = request.files['filename']

    # Zeichenkodierung aus dem Formular auslesen
    encoding = request.form['encoding']
    if encoding == 'utf-16':
        csv_data = csv_file.read().decode('utf-16')
    elif encoding == 'utf-8':
        csv_data = csv_file.read().decode('utf-8')
    elif encoding == 'ANSI':
        csv_data = csv_file.read().decode('latin-1')


    skip_rows = list(range(0, 65)) + [66]

    # Trennzeichen aus dem Formular auslesen
    delimiter = request.form['delimiter']
    if delimiter == 'tab':
        delimiter = '\t'
    elif delimiter == 'semicolon':
        delimiter = ';'

    # Dezimaltrennzeichen aus dem Formular auslesen
    decimal_separator = request.form['decimal_separator']
    if decimal_separator == 'dot':
        decimal_separator = '.'
    elif decimal_separator == 'comma':
        decimal_separator = ','

    # CSV-Daten in ein DataFrame laden
    df = pd.read_csv(io.StringIO(csv_data), delimiter=delimiter, decimal=decimal_separator, skiprows=skip_rows, skipfooter=1, engine='python')

    df = df.iloc[1:, :]
    # rename column
    df.rename(columns = {'Scan-X':'Distanz (m)'}, inplace = True)
    # convert distance to numeric value  
    df['Distanz (m)'] = pd.to_numeric(df['Distanz (m)'], errors='coerce')

    # Add Empty rows for missing distance.

    #  distance
    #avg_distance = 0.05 #default = 0.05
    avg_distance = float(request.form['avg_spacing'])


    # Create a new DataFrame to store the modified rows
    new_df = pd.DataFrame(columns=df.columns)

    # 1000er Trennzeichen ignorieren
    for column in new_df.columns:
        new_df[column] = new_df[column].str.replace("'", "")

    # Iterate over the rows of the original DataFrame
    for index, row in df.iterrows():
        # Add the current row to the new DataFrame
        # new_df = pd.concat([new_df, row], axis = 0)
        new_df = pd.concat([new_df, pd.DataFrame([row])], ignore_index=True)
        
        # Check if the distance between the current row and the next row is greater than average distance
        if index < len(df) - 1 and df.at[index + 1, 'Distanz (m)'] - row['Distanz (m)'] > avg_distance:
            # Calculate the number of empty rows needed
            num_empty_rows = int((df.at[index + 1, 'Distanz (m)'] - row['Distanz (m)']) / avg_distance) - 1
            
            # Insert the empty rows and increment the distance
            for i in range(1, num_empty_rows + 1):
                empty_row = row.copy()  # Create a copy of the current row
                empty_row['Distanz (m)'] += avg_distance * i  # Increment the distance
                #new_df = new_df.append(empty_row, ignore_index=True)
                new_df = pd.concat([new_df, pd.DataFrame([empty_row])], ignore_index=True)

    new_df = pd.merge(new_df['Distanz (m)'], df, on ='Distanz (m)', how = 'left')
    # Drop those columns where there are null values
    new_df.dropna(axis=1, how='all', inplace = True)
    # Drop those rows where there are all null values
    new_df = new_df.dropna(axis=0, how = 'all')

    # Convert distance column to float if necessary
    new_df['Distanz (m)'] = pd.to_numeric(new_df['Distanz (m)'], errors='coerce')
    new_df.set_index('Distanz (m)', inplace = True)
    
    # Convert line columns to float if necessary
    line_columns = [col for col in new_df.columns if col.startswith('Line')]
    new_df[line_columns] = new_df[line_columns].apply(pd.to_numeric, errors='coerce')


    
    # Leere Felder interpolieren
    interpolation_option = request.form.get('interpolation')

    # Interpolation entsprechend der ausgewählten Option ein- oder ausschalten
    if interpolation_option == 'on':
        new_df = new_df.interpolate(limit_direction='both', limit_area='inside')
        interpolation = request.form['interpolation_dropdown']
        
    else:
        # Keine Interpolation durchführen
        interpolation = 'none'
        pass

    # Create a transpose of the DataFrame with only the line and distance columns
    transposed_df = new_df[line_columns].transpose()

    # Anzahl Linien und Meter bestimmen
    num_lines = len(new_df.columns)
    num_meters = len(new_df)

    # Größe der Figur und Seitenverhältnis anpassen
    max_width = 20
    max_height = 10
    aspect_ratio = num_meters / num_lines

    fig_height = min(max_height, num_lines)
    fig_width = min(max_width, fig_height * aspect_ratio)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Farbskala definieren
    cmap_choice = request.form['cmap_dropdown']

    if cmap_choice == 'custom_cmap':
        # Farbwerte aus dem Formular auslesen
        color1 = request.form['color1']
        color2 = request.form['color2']
        color3 = request.form['color3']
        color4 = request.form['color4']
        color5 = request.form['color5']
        color6 = request.form['color6']
        

        # Schritte für die Farbskala aus dem Formular auslesen
        step1 = float(request.form['step1'])
        step2 = float(request.form['step2'])
        step3 = float(request.form['step3'])
        step4 = float(request.form['step4'])
        step5 = float(request.form['step5'])
        step6 = float(request.form['step6'])
        
        # Benutzerdefinierte diskrete Farben und Wertebereiche
        colors = [color1, color2, color3, color4, color5, color6]
        bounds = [step1, step2, step3, step4, step5, step6, 90]
        cmap = ListedColormap(colors)
        norm = BoundaryNorm(bounds, cmap.N)
        # sns.heatmap(transposed_df, cmap=cmap, cbar_kws={'label': 'Value'}, mask=transposed_df.isnull(), norm=norm)
        im = ax.imshow(transposed_df, cmap=cmap,aspect='auto', norm=norm)

    else:
        # Standardmäßige Farbskala verwenden
        cmap = plt.cm.get_cmap(cmap_choice)
        # sns.heatmap(transposed_df, cmap=cmap, vmin=0, vmax=90, cbar_kws={'label': 'Value'}, mask=transposed_df.isnull())

        im = ax.imshow(transposed_df, cmap=cmap, aspect='auto', interpolation=interpolation)
 
        
    # Set x-axis ticks and labels
    num_ticks = 10  # Number of ticks on the x-axis
    tick_positions = np.linspace(0, len(new_df.index)-1, num_ticks, dtype=int)
    tick_labels = new_df.index[tick_positions]

    plt.xticks(tick_positions, tick_labels, rotation=45, ha='right')

    # Set x-axis ticks and labels with equal gap
    num_ticks = 10  # Number of ticks on the x-axis
    tick_positions = np.linspace(0, len(new_df.index)-1, num_ticks, dtype=int)
    tick_labels = new_df.index[tick_positions]

    # Round each element in the tick_labels
    tick_labels = [round(num, 3) for num in tick_labels]


    plt.xticks(tick_positions, tick_labels, rotation=45, ha='right')

    plt.colorbar(im, label='Betonüberdeckung in mm')
    plt.xlabel('Distance')
    plt.ylabel('Lines')
    plt.title('Heatmap of Lines and Distance')
    plt.xticks(rotation=90, ha='right') 
    plt.yticks(rotation=0, ha='right')# Adjust the rotation angle and alignment as needed
    plt.tight_layout()  # Adjust spacing for labels

    # Generierte Heatmap als Bytes-Objekt speichern
    heatmap_bytes = io.BytesIO()
    plt.savefig(heatmap_bytes, format='png', dpi=300)
    plt.close(fig)
    heatmap_bytes.seek(0)

    # Heatmap-Bytes in eine temporäre Datei speichern
    temp_filename = 'heatmap.png'
    with open(temp_filename, 'wb') as temp_file:
        temp_file.write(heatmap_bytes.read())

    # URL für Heatmap-Anzeige und Download erstellen
    heatmap_url = url_for('static', filename=temp_filename)
    download_url = url_for('download_heatmap', filename=temp_filename)
    

     # Create a response and set cache control header to no-cache
    response = make_response(heatmap_bytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Cache-Control'] = 'no-cache'

    # Clear the current figure to release memory
    plt.clf()

    return render_template('heatmap.html', heatmap_url=heatmap_url, download_url=download_url, image_data=heatmap_bytes.getvalue())
    # return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
