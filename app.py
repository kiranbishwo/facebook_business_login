# Facebook Business Page Full Access Login App

import os
from flask import Flask, redirect, request, session, render_template
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Facebook App Configuration
FACEBOOK_APP_ID = 'your_app_id'
FACEBOOK_APP_SECRET = 'your_app_secret'
REDIRECT_URI = 'http://localhost:5000/facebook-callback'
GRAPH_API_VERSION = 'v19.0'

@app.route('/')
def index():
    """Main page with Facebook login button"""
    return render_template('index.html', 
        facebook_app_id=FACEBOOK_APP_ID, 
        redirect_uri=REDIRECT_URI)

@app.route('/login')
def facebook_login():
    """Redirect to Facebook OAuth login"""
    facebook_login_url = (
        f"https://www.facebook.com/{GRAPH_API_VERSION}/dialog/oauth?"
        f"client_id={FACEBOOK_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        # Extended permissions for page management
        "&scope=pages_show_list,pages_read_engagement,pages_messaging,"
        "pages_manage_posts,pages_manage_engagement,pages_manage_ads,"
        "pages_read_user_content,business_management"
        "&response_type=code"
    )
    return redirect(facebook_login_url)

@app.route('/facebook-callback')
def facebook_callback():
    """Handle Facebook OAuth callback and token generation"""
    # Get authorization code from callback
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization failed", 400

    # Exchange authorization code for access token
    token_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
    token_params = {
        'client_id': FACEBOOK_APP_ID,
        'client_secret': FACEBOOK_APP_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': auth_code
    }

    # Request access token
    token_response = requests.get(token_url, params=token_params)
    
    if token_response.status_code != 200:
        return f"Token request failed: {token_response.text}", 400
    
    access_token = token_response.json().get('access_token')
    
    # Get user's pages with extended fields
    pages_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/accounts"
    pages_params = {
        'access_token': access_token,
        'fields': 'id,name,access_token,category,tasks,cover,picture'
    }
    
    pages_response = requests.get(pages_url, params=pages_params)
    
    if pages_response.status_code != 200:
        return f"Pages fetch failed: {pages_response.text}", 400
    
    pages_data = pages_response.json().get('data', [])
    
    # Store tokens and page info in session
    session['access_token'] = access_token
    session['pages'] = pages_data

    return render_template('pages.html', pages=pages_data)

@app.route('/select_page', methods=['POST'])
def select_page():
    """Select and get full access to a specific page"""
    if 'pages' not in session:
        return redirect('/login')
    
    page_id = request.form.get('page_id')
    if not page_id:
        return "No page selected", 400
    
    # Find the selected page and its access token
    selected_page = None
    for page in session.get('pages', []):
        if page['id'] == page_id:
            selected_page = page
            break
    
    if not selected_page:
        return "Page not found", 404
    
    # Page access token
    page_access_token = selected_page['access_token']
    
    # Perform comprehensive page operations
    try:
        # 1. Get Page Information
        page_info_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}"
        page_info_params = {
            'access_token': page_access_token,
            'fields': 'id,name,about,category,description,emails,phone,website,hours'
        }
        page_info_response = requests.get(page_info_url, params=page_info_params)
        page_info = page_info_response.json()
        
        # 2. Get Page Posts
        posts_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/posts"
        posts_params = {
            'access_token': page_access_token,
            'fields': 'message,created_time,full_picture,likes.summary(true),comments.summary(true)'
        }
        posts_response = requests.get(posts_url, params=posts_params)
        posts_data = posts_response.json().get('data', [])
        
        # 3. Get Page Insights (if available)
        insights_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/insights"
        insights_params = {
            'access_token': page_access_token,
            'metric': 'page_views_total,page_impressions_unique,page_engaged_users'
        }
        insights_response = requests.get(insights_url, params=insights_params)
        insights_data = insights_response.json().get('data', [])
        
        # 4. Get Page Conversations
        conversations_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/conversations"
        conversations_params = {
            'access_token': page_access_token,
            'fields': 'participants,messages,updated_time'
        }
        conversations_response = requests.get(conversations_url, params=conversations_params)
        conversations_data = conversations_response.json().get('data', [])
        
        return render_template('page_details.html', 
            page_info=page_info, 
            posts=posts_data, 
            insights=insights_data,
            conversations=conversations_data)
    
    except Exception as e:
        return f"Error accessing page: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)