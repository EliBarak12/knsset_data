from flask import Flask, request, jsonify, abort
from kns_data import *
import sqlite3
import json

app = Flask(__name__)


SECRET_API_KEY = '3ca62a2ad87376be2697209a1770e1afdbbba220'

def authenticate_request():
    api_key = request.headers.get('Authorization')

    if api_key != SECRET_API_KEY:
        abort(401)

def update_bill_vote(data):
    conn = sqlite3.connect("bills_database1.db")
    cursor = conn.cursor()
    bill_id_to_update = data['BillID']
    vote_to_up = data['vote']
    cursor.execute("UPDATE bills SET TotalVotes = TotalVotes + 1, " + vote_to_up + " = "+vote_to_up+" + 1 WHERE BillID = ?",
                   (bill_id_to_update,))

    conn.commit()
    conn.close()
def update_parties_vote(data):
    conn = sqlite3.connect("billsParties_database1.db")
    cursor = conn.cursor()
    bill_id_to_update = data['BillID']
    party_to_up = data['party']
    cursor.execute(
        "UPDATE BillPart SET  " + party_to_up + " = " + party_to_up + "+ 1 WHERE BillID = ?",
        (bill_id_to_update,))

    conn.commit()
    conn.close()

def sort_bills_by_interest(data):
    sorted_data = sorted(data, key=lambda x: x['total_vote'], reverse=True)
    return sorted_data


@app.route('/api/update_data', methods=['POST'])
def update_data():
    try:
        authenticate_request()
        data = request.get_json()

        update_bill_vote(data)
        update_parties_vote(data)



        response = {'message': 'Data updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        error_response = {'error': str(e)}
        return jsonify(error_response), 500

def get_data_bills_from_db():
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
            'total_vote': row[6],
            'in_favor': row[7],
            'against': row[8]
        })

    return data

def get_data_parties_from_db():
    conn = sqlite3.connect("billsParties_database1.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM BillPart ')
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'BillID': row[0],
            'Likud_For': row[1],
            'Likud_Against': row[2],
            'YeshAtidNationalUnity_For': row[3],
            'YeshAtidNationalUnity_Against': row[4],
            'Shas_For': row[5],
            'Shas_Against': row[6],
            'Mafdal_ReligiousZionism_For': row[7],
            'Mafdal_ReligiousZionism_Against': row[8],
            'UnitedTorahJudaism_For': row[9],
            'UnitedTorahJudaism_Against':row[10],
            'OtzmaYehudit_For':row[11],
            'OtzmaYehudit_Against':row[12],
            'YisraelBeiteinu_For':row[13],
            'YisraelBeiteinu_Against':row[14],
            'UnitedArabList_For':row[15],
            'UnitedArabList_Against':row[16],
            'Hadash_Taal_For':row[17],
            'Hadash_Taal_Against':row[18],
            'LaborParty_For':row[19],
            'LaborParty_Against':row[20],
            'Noam_For':row[21],
            'Noam_Against':row[22]
        })

    return data



@app.route('/api/data_bills', methods=['GET'])
def api_data():
    data = get_data_bills_from_db()
    sorted_data = sort_bills_by_interest(data)
    response = json.dumps(sorted_data, ensure_ascii=False).encode('utf8')
    return response


@app.route('/api/data_parties', methods=['GET'])
def api_data_parties():
    data = get_data_parties_from_db()
    response = json.dumps(data, ensure_ascii=False).encode('utf8')
    return response


if __name__ == '__main__':
    app.run(debug=True)



