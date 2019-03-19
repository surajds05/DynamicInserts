from flask import Flask, render_template, url_for, redirect, request
from forms import InputsForm
import OracleConnect

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
def home():
    form = InputsForm()
    if form.validate_on_submit():
        return redirect(url_for('fetchChildTables', parent_table=form.parentTableName.data, recordCnt=form.recordCnt.data, varcharPrefix=form.varcharPrefix.data, beginDttm=form.beginDttm.data))
    return render_template('inputsform.html', form=form)


@app.route('/childTables/<parent_table>/<recordCnt>/<varcharPrefix>/<beginDttm>', methods=['GET', 'POST'])
def fetchChildTables(parent_table, recordCnt, varcharPrefix, beginDttm):
    child_tables = OracleConnect.returnChildTables(parent_table)
    if request.method == 'POST':
        child_tables_selected = request.form.getlist('childTables')

        return redirect(url_for('displayOutputInserts', parent_table=parent_table, recordCnt=recordCnt, varcharPrefix=varcharPrefix, beginDttm=beginDttm, child_tables=child_tables_selected))
    return render_template('childTables.html', child_tables=child_tables)

@app.route('/insert/<parent_table>/<recordCnt>/<varcharPrefix>/<beginDttm>/<child_tables>', methods=['GET', 'POST'])
def displayOutputInserts(parent_table, recordCnt, varcharPrefix, beginDttm, child_tables):
    parent_table = parent_table
    child_tables = child_tables.replace("'",'').replace(" ",'').strip('[]')
    child_tables_list = child_tables.split(',')
    loop_cntr = recordCnt
    varchar_prefix = varcharPrefix
    begin_dttm = beginDttm[5:7]+beginDttm[8:10]+beginDttm[0:4]

    pkg_output = OracleConnect.insertData(parent_table, child_tables_list, loop_cntr, varchar_prefix, begin_dttm)
    return render_template('outputInserts.html', output=pkg_output)



if __name__ == '__main__':
    app.run(debug=True)