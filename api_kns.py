from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def get_data_from_db():
    conn = sqlite3.connect('bills_database1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bills')
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'BillID': row[0],
            'name': row[1],
            'SummaryLaw': row[2],
            'LastUpdatedDate': row[3],
            'document': row[4],
            'present': row[5],
            'total_vote':row[6],
            'in_favor': row[7],
            'against':row[8]
        })

    return data

@app.route('/api/data_kns', methods=['GET'])
def api_data():
    data = get_data_from_db()
    print(len(data))
    response = json.dumps(data, ensure_ascii=False).encode('utf8')

    return response

if __name__ == '__main__':
    app.run(debug=True)
