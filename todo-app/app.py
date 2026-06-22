from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)
todos = []
next_id = 1
HTML = '''<!DOCTYPE html><html><head><title>Todo</title></head><body>
<h1>Todo List</h1>
<form id="f"><input id="t" placeholder="Task" required><button>Add</button></form>
<ul id="l"></ul>
<script>
async function load(){const r=await fetch('/todos'); const todos=await r.json(); const ul=document.getElementById('l'); ul.innerHTML=''; todos.forEach(t=>{const li=document.createElement('li'); li.textContent=t.task+' '; const btn=document.createElement('button'); btn.textContent='Delete'; btn.onclick=async()=>{await fetch('/todos/'+t.id,{method:'DELETE'}); load();}; li.appendChild(btn); ul.appendChild(li);});}
document.getElementById('f').onsubmit=async(e)=>{e.preventDefault(); const task=document.getElementById('t').value; await fetch('/todos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task})}); document.getElementById('t').value=''; load();};
load();
</script></body></html>'''
@app.route('/')
def index(): return render_template_string(HTML)
@app.route('/todos', methods=['GET'])
def get(): return jsonify(todos)
@app.route('/todos', methods=['POST'])
def add():
    global next_id
    data=request.json
    todo={'id':next_id,'task':data['task'],'completed':False}
    todos.append(todo); next_id+=1; return jsonify(todo),201
@app.route('/todos/<int:tid>', methods=['DELETE'])
def delete(tid):
    global todos
    todos=[t for t in todos if t['id']!=tid]
    return '',204
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)