from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from datetime import datetime
from statistics import mean
import uuid
import json
import os
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Try to connect to MySQL, fallback to file storage if fails
DB_AVAILABLE = False
try:
    from flask_mysqldb import MySQL
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'your_password'
    app.config['MYSQL_DB'] = 'eval'
    
    mysql = MySQL(app)
    # Test connection
    cur = mysql.connection.cursor()
    cur.execute("SELECT 1")
    cur.close()
    DB_AVAILABLE = True
    print("MySQL connected successfully")
except Exception as e:
    print(f"MySQL not available: {e}")
    print("Using file-based storage fallback")
    DB_AVAILABLE = False


#DUMMY DATA STARTS
# FOR TRYING ONLY, CAN BE DELETED ONCE A DB CONNECTION IS ESTABLISHED!
DATA_FILE = 'data_store.json'

def get_default_data():
    return {
        'participants': {},
        'responses': {},
        'admin_users': {
            'ADMIN': {'password': 'admin123', 'full_name': 'Administrator', 'is_master_admin': True},
            'TRAINER1': {'password': 'trainer123', 'full_name': 'TRAINER 1', 'is_master_admin': False},
            'TRAINER2': {'password': 'trainer123', 'full_name': 'TRAINER 2', 'is_master_admin': False},
            'TRAINER3': {'password': 'trainer123', 'full_name': 'TRAINER 3', 'is_master_admin': False},
            'TRAINER4': {'password': 'trainer123', 'full_name': 'TRAINER 4', 'is_master_admin': False},
        },
        'criteria': {
            'Section 1: Teaching Skills': [
                {'id': 1, 'question': 'The trainer demonstrates mastery of the subject matter.'},
                {'id': 2, 'question': 'The trainer explains concepts clearly and effectively.'},
                {'id': 3, 'question': 'The trainer uses appropriate teaching methods and techniques.'},
            ],
            'Section 2: Communication Skills': [
                {'id': 4, 'question': 'The trainer communicates effectively with trainees.'},
                {'id': 5, 'question': 'The trainer listens and responds to trainee questions.'},
                {'id': 6, 'question': 'The trainer provides constructive feedback.'},
            ],
            'Section 3: Training Materials': [
                {'id': 7, 'question': 'Training materials are relevant and up-to-date.'},
                {'id': 8, 'question': 'Training materials are easy to understand.'},
                {'id': 9, 'question': 'Training materials support the learning objectives.'},
            ],
            'Section 4: Trainee Satisfaction': [
                {'id': 10, 'question': 'I am satisfied with the overall training experience.'},
                {'id': 11, 'question': 'The training met my expectations.'},
                {'id': 12, 'question': 'I would recommend this training to others.'},
            ],
        },
        'sections': [
            {'id': 1, 'name': 'Section 1: Teaching Skills'},
            {'id': 2, 'name': 'Section 2: Communication Skills'},
            {'id': 3, 'name': 'Section 3: Training Materials'},
            {'id': 4, 'name': 'Section 4: Trainee Satisfaction'},
        ]
    }

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return get_default_data()
    return get_default_data()

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

# Load fallback data
fallback_data = load_data()

#DUMMY DATA ENDS HERE

def get_next_id():
    return str(uuid.uuid4())[:8]

def get_criteria_by_section():
    section_criteria = {}
    for section in fallback_data['sections']:
        section_criteria[section['name']] = [
            (c['id'], c['question']) 
            for c in fallback_data['criteria'].get(section['name'], [])
        ]
    return section_criteria

def get_batch_summary(trainer_name, training_duration, qualification):
    participants = []
    comments_by_participant = {}
    
    for pid, pdata in fallback_data['participants'].items():
        if (pdata['trainer_name'] == trainer_name and 
            pdata['training_duration'] == training_duration and 
            pdata['qualification'] == qualification):
            participants.append(pdata['name'])
            comments_by_participant[pdata['name']] = pdata.get('comments', '')
    
    if not participants:
        return {
            'participants': [],
            'sections': [],
            'comments': [],
            'total_points': 0,
            'batch_average': 0,
            'total_questions': 0
        }
    
    sections_data = []
    total_points = 0
    total_questions = 0
    all_question_averages = []
    
    for section in fallback_data['sections']:
        section_name = section['name']
        questions = {}
        section_points = 0
        section_question_averages = []
        
        for c in fallback_data['criteria'].get(section_name, []):
            criterion_id = c['id']
            question_text = c['question']
            questions[question_text] = {'ratings': {}}
            
            for pid, pdata in fallback_data['participants'].items():
                if (pdata['trainer_name'] == trainer_name and 
                    pdata['training_duration'] == training_duration and 
                    pdata['qualification'] == qualification):
                    response_key = f"{pid}_{criterion_id}"
                    if response_key in fallback_data['responses']:
                        rating = fallback_data['responses'][response_key]
                        questions[question_text]['ratings'][pdata['name']] = rating
                        section_points += rating
            
            if questions[question_text]['ratings']:
                avg = mean(questions[question_text]['ratings'].values())
                questions[question_text]['average'] = round(avg, 2)
                section_question_averages.append(avg)
                all_question_averages.append(avg)
                total_questions += 1
        
        section_average = round(mean(section_question_averages), 2) if section_question_averages else 0
        total_points += section_points
        
        sections_data.append({
            'name': section_name,
            'questions': questions,
            'section_points': section_points,
            'section_average': section_average,
            'average_per_group': section_average
        })
    
    comments_list = [(name, comments_by_participant.get(name, 'No comments')) for name in participants]
    batch_average = round(mean(all_question_averages), 2) if all_question_averages else 0
    
    return {
        'participants': participants,
        'sections': sections_data,
        'comments': comments_list,
        'total_points': total_points,
        'batch_average': batch_average,
        'total_questions': total_questions
    }

@app.context_processor
def inject_admin():
    return {'admin_is_on': session.get('admin_logged_in', False)}

@app.route('/', methods=['GET', 'POST'])
def eval_form():
    try:
        if request.method == 'POST':
            name = request.form['name'].strip()
            trainer_name = request.form['trainer_name']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            training_duration = f"{start_date} to {end_date}"
            qualification = request.form['qualification']
            
            # Check for duplicate
            for pid, pdata in fallback_data['participants'].items():
                if (pdata['name'] == name and 
                    pdata['trainer_name'] == trainer_name and 
                    pdata['training_duration'] == training_duration):
                    flash("You've already submitted an evaluation for this trainer in this batch.", "danger")
                    return redirect(url_for('already_submitted', name=name))
            
            participant_id = get_next_id()
            comments = "" if request.form['comment_option'] == 'NONE' else request.form.get('comments', '')
            
            fallback_data['participants'][participant_id] = {
                'name': name,
                'qualification': qualification,
                'program_type': request.form['program_type'],
                'training_duration': training_duration,
                'trainer_name': trainer_name,
                'evaluation_date': request.form['evaluation_date'],
                'comments': comments
            }
            
            for key, rating in request.form.items():
                if key.startswith("criterion_"):
                    criterion_id = int(key.split("_")[1])
                    response_key = f"{participant_id}_{criterion_id}"
                    fallback_data['responses'][response_key] = int(rating)
            
            save_data(fallback_data)
            return redirect(url_for('thank_you', name=name))
        
        return render_template('form.html', section_criteria=get_criteria_by_section())
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return render_template('form.html', section_criteria=get_criteria_by_section())

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', name=request.args.get('name'))

@app.route('/already_submitted')
def already_submitted():
    return render_template('already_submitted.html', name=request.args.get('name'))

@app.route('/view/<name>')
def view_submission(name):
    try:
        participant = None
        pid = None
        for p_id, pdata in fallback_data['participants'].items():
            if pdata['name'] == name:
                participant = pdata
                pid = p_id
                break
        
        if not participant:
            abort(404)
        
        section_criteria = {}
        total_points = 0
        
        for section in fallback_data['sections']:
            section_name = section['name']
            section_data = []
            for c in fallback_data['criteria'].get(section_name, []):
                response_key = f"{pid}_{c['id']}"
                rating = fallback_data['responses'].get(response_key, 0)
                section_data.append((c['question'], rating))
                total_points += rating
            section_criteria[section_name] = section_data
        
        participant_tuple = (
            pid,
            participant['qualification'],
            participant['program_type'],
            participant['training_duration'],
            participant['trainer_name'],
            participant['evaluation_date'],
            participant.get('comments', '')
        )
        
        return render_template('view_submission.html',
                             name=name,
                             participant=participant_tuple,
                             section_criteria=section_criteria,
                             total_points=total_points,
                             admin_view=request.args.get('admin') == '1')
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('eval_form'))

@app.route('/admin')
def admin():
    try:
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        
        batch_data = {}
        current_trainer = session.get('full_name')
        is_master_admin = session.get('is_master_admin', False)
        
        # Group participants by batch
        batches = {}
        for pid, pdata in fallback_data['participants'].items():
            trainer = pdata['trainer_name']
            duration = pdata['training_duration']
            qual = pdata['qualification']
            
            if is_master_admin:
                batch_key = f"Batch ['{duration}'] - {qual}"
                if batch_key not in batches:
                    batches[batch_key] = {
                        'trainer_name': trainer,
                        'qualification': qual,
                        'participants': []
                    }
                batches[batch_key]['participants'].append(pdata['name'])
            else:
                if trainer == current_trainer:
                    batch_key = f"Batch {duration} {qual}"
                    if batch_key not in batches:
                        batches[batch_key] = {
                            'trainer_name': trainer,
                            'qualification': qual,
                            'participants': []
                        }
                    batches[batch_key]['participants'].append(pdata['name'])
        
        # Get summaries for each batch
        for batch_name, batch_info in batches.items():
            if ' - ' in batch_name:
                duration_part = batch_name.split(' - ')[0].replace('Batch [', '').replace(']', '')
            else:
                parts = batch_name.split(' ')
                duration_part = parts[1] + ' ' + parts[2] + ' ' + parts[3]
            
            summary = get_batch_summary(
                batch_info['trainer_name'],
                duration_part,
                batch_info['qualification']
            )
            batch_data[batch_name] = {
                'participants': batch_info['participants'],
                'summary': summary,
                'trainer_name': batch_info['trainer_name'],
                'qualification': batch_info['qualification']
            }
        
        return render_template('admin.html', 
                             batch_data=batch_data,
                             current_trainer=current_trainer)
    except Exception as e:
        flash(f"Error loading admin panel: {str(e)}", "danger")
        return render_template('admin.html', batch_data={}, current_trainer=session.get('full_name', 'Unknown'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    try:
        if request.method == 'POST':
            username = request.form['username'].strip().upper()
            password = request.form['password']
            
            if username in fallback_data['admin_users']:
                admin = fallback_data['admin_users'][username]
                if admin['password'] == password:
                    session['admin_logged_in'] = True
                    session['username'] = username
                    session['full_name'] = admin['full_name']
                    session['is_master_admin'] = admin['is_master_admin']
                    return redirect(url_for('admin'))
            
            error = "Invalid credentials"
    except Exception as e:
        error = f"Login error: {str(e)}"
    
    return render_template('admin_login.html', error=error)

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        if 'admin_logged_in' not in session:
            abort(403)
        
        is_master_admin = session.get('is_master_admin', False)
        trainer_name = session.get('full_name')
        
        if is_master_admin:
            fallback_data['participants'] = {}
            fallback_data['responses'] = {}
            flash("All evaluations have been cleared.", "success")
        else:
            to_delete = []
            for pid, pdata in fallback_data['participants'].items():
                if pdata['trainer_name'] == trainer_name:
                    to_delete.append(pid)
            
            for pid in to_delete:
                del fallback_data['participants'][pid]
                for key in list(fallback_data['responses'].keys()):
                    if key.startswith(f"{pid}_"):
                        del fallback_data['responses'][key]
            
            flash("Your evaluations have been cleared.", "info")
        
        save_data(fallback_data)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for('admin'))

@app.route('/delete_submission/<name>', methods=['POST'])
def delete_submission(name):
    try:
        if 'admin_logged_in' not in session:
            abort(403)
        
        to_delete_pid = None
        for pid, pdata in fallback_data['participants'].items():
            if pdata['name'] == name:
                to_delete_pid = pid
                break
        
        if to_delete_pid:
            del fallback_data['participants'][to_delete_pid]
            for key in list(fallback_data['responses'].keys()):
                if key.startswith(f"{to_delete_pid}_"):
                    del fallback_data['responses'][key]
            flash(f"Deleted evaluation for {name}", "info")
            save_data(fallback_data)
        else:
            flash("Participant not found", "danger")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for('admin'))

@app.route('/trainer_ratings')
def trainer_ratings():
    try:
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        
        ratings_data = {}
        is_master_admin = session.get('is_master_admin', False)
        
        if is_master_admin:
            trainer_ratings = {}
            for pid, pdata in fallback_data['participants'].items():
                trainer = pdata['trainer_name']
                qual = pdata['qualification']
                
                if trainer not in trainer_ratings:
                    trainer_ratings[trainer] = {}
                
                if qual not in trainer_ratings[trainer]:
                    trainer_ratings[trainer][qual] = {'ratings': [], 'count': 0}
                
                all_criteria = []
                for section in fallback_data['sections']:
                    all_criteria.extend(fallback_data['criteria'].get(section['name'], []))
                
                for c in all_criteria:
                    response_key = f"{pid}_{c['id']}"
                    if response_key in fallback_data['responses']:
                        trainer_ratings[trainer][qual]['ratings'].append(fallback_data['responses'][response_key])
                        trainer_ratings[trainer][qual]['count'] += 1
            
            for trainer in trainer_ratings:
                ratings_data[trainer] = {'overall': 0}
                all_criteria_count = sum(len(fallback_data['criteria'].get(s['name'], [])) for s in fallback_data['sections'])
                
                for qual, data in trainer_ratings[trainer].items():
                    if data['ratings']:
                        avg = mean(data['ratings'])
                        ratings_data[trainer][qual] = {
                            'average': round(avg, 2),
                            'count': data['count'] // all_criteria_count if all_criteria_count > 0 else 1
                        }
                
                quals = [v['average'] for k, v in ratings_data[trainer].items() if k != 'overall']
                ratings_data[trainer]['overall'] = round(sum(quals)/len(quals), 2) if quals else 0
        
        else:
            trainer_name = session.get('full_name')
            qual_ratings = {}
            all_criteria_count = sum(len(fallback_data['criteria'].get(s['name'], [])) for s in fallback_data['sections'])
            
            for pid, pdata in fallback_data['participants'].items():
                if pdata['trainer_name'] == trainer_name:
                    qual = pdata['qualification']
                    if qual not in qual_ratings:
                        qual_ratings[qual] = {'ratings': [], 'count': 0}
                    
                    for section in fallback_data['sections']:
                        for c in fallback_data['criteria'].get(section['name'], []):
                            response_key = f"{pid}_{c['id']}"
                            if response_key in fallback_data['responses']:
                                qual_ratings[qual]['ratings'].append(fallback_data['responses'][response_key])
                                qual_ratings[qual]['count'] += 1
            
            for qual, data in qual_ratings.items():
                if data['ratings']:
                    ratings_data[qual] = {
                        'average': round(mean(data['ratings']), 2),
                        'count': data['count'] // all_criteria_count if all_criteria_count > 0 else 1
                    }
        
        return render_template('trainer_ratings.html',
                             trainer_ratings=ratings_data,
                             is_master_admin=is_master_admin)
    except Exception as e:
        flash(f"Error loading ratings: {str(e)}", "danger")
        return render_template('trainer_ratings.html', trainer_ratings={}, is_master_admin=False)

@app.route('/leaderboard')
def leaderboard():
    try:
        if 'admin_logged_in' not in session or not session.get('is_master_admin'):
            return redirect(url_for('admin_login'))
        
        trainer_scores = {}
        qual_scores = {}
        all_criteria_count = sum(len(fallback_data['criteria'].get(s['name'], [])) for s in fallback_data['sections'])
        
        for pid, pdata in fallback_data['participants'].items():
            trainer = pdata['trainer_name']
            qual = pdata['qualification']
            
            if trainer not in trainer_scores:
                trainer_scores[trainer] = {'ratings': [], 'quals': set()}
            
            if qual not in qual_scores:
                qual_scores[qual] = {}
            if trainer not in qual_scores[qual]:
                qual_scores[qual][trainer] = {'ratings': [], 'count': 0}
            
            trainer_scores[trainer]['quals'].add(qual)
            
            for section in fallback_data['sections']:
                for c in fallback_data['criteria'].get(section['name'], []):
                    response_key = f"{pid}_{c['id']}"
                    if response_key in fallback_data['responses']:
                        rating = fallback_data['responses'][response_key]
                        trainer_scores[trainer]['ratings'].append(rating)
                        qual_scores[qual][trainer]['ratings'].append(rating)
                        qual_scores[qual][trainer]['count'] += 1
        
        overall_leaderboard = []
        for trainer, data in trainer_scores.items():
            if data['ratings']:
                overall_leaderboard.append({
                    'name': trainer,
                    'avg_rating': round(mean(data['ratings']), 2),
                    'eval_count': len(data['ratings']) // all_criteria_count if all_criteria_count > 0 else 1,
                    'qual_count': len(data['quals'])
                })
        
        overall_leaderboard.sort(key=lambda x: x['avg_rating'], reverse=True)
        overall_leaderboard = overall_leaderboard[:10]
        
        qual_leaderboards = {}
        for qual, trainers in qual_scores.items():
            qual_leaderboards[qual] = []
            for trainer, data in trainers.items():
                if data['ratings']:
                    qual_leaderboards[qual].append({
                        'name': trainer,
                        'avg_rating': round(mean(data['ratings']), 2),
                        'eval_count': data['count'] // all_criteria_count if all_criteria_count > 0 else 1
                    })
            qual_leaderboards[qual].sort(key=lambda x: x['avg_rating'], reverse=True)
            qual_leaderboards[qual] = qual_leaderboards[qual][:10]
        
        return render_template('leaderboard.html',
                             overall_leaderboard=overall_leaderboard,
                             qual_leaderboards=qual_leaderboards)
    except Exception as e:
        flash(f"Error loading leaderboard: {str(e)}", "danger")
        return render_template('leaderboard.html', overall_leaderboard=[], qual_leaderboards={})

@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)