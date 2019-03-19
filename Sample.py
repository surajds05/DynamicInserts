from flask import Flask, render_template, url_for, redirect, request
from forms import InputsForm
import OracleConnect

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
def home():
    form = InputsForm()
    if form.validate_on_submit():
        return redirect(url_for('fetchChildTables', parent_table=form.parentTableName.data, recordCnt=form.recordCnt.data, varcharPrefix=form.varcharPrefix.data, beginDttm=form.beginDttm.data, form=form))
    return render_template('result.html', form=form)


@app.route('/childTables/<parent_table>/<recordCnt>/<varcharPrefix>/<beginDttm>/<form>', methods=['GET', 'POST'])
def fetchChildTables(parent_table, recordCnt, varcharPrefix, beginDttm, form):
    child_tables = OracleConnect.returnChildTables(parent_table)
    if request.method == 'POST':
        child_tables_selected = request.form.getlist('childTables')

        return redirect(url_for('displayOutputInserts', parent_table=parent_table, recordCnt=recordCnt, varcharPrefix=varcharPrefix, beginDttm=beginDttm, child_tables=child_tables_selected))
    return render_template('result.html', child_tables=child_tables, displayChildTables=True, form=form)

if __name__ == '__main__':
    app.run(debug=True)