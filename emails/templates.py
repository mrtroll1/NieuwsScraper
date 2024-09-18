# Templates for email composing

article_template = """
<div style="margin-bottom: 15px; padding: 5px; border: 0; border-radius: 5px; text-align: center; max-width: 50%; margin: 0 auto;">
    <a href="{{ url }}" style="text-decoration: none; color: #000; cursor: pointer;">
        <h2 style="margin-top: 10px; font-size: 16px; text-align: center; max-width: 70%; margin: 0 auto; word-wrap: break-word; transition: text-decoration 0.15s;">{{ title }}</h2>
        <img src="{{ photo_url }}" alt="{{ title }}" style="width: 100%; max-width: 400px; border-radius: 5px; border: 3px solid #d17dc0; display: block; margin: 0 auto; margin-bottom: 10px;"/>
        <p style="text-align: center; max-width: 70%; margin: 0 auto; margin-bottom: 30px !important; word-wrap: break-word; transition: text-decoration 0.15s;">{{ description }}</p>

</div>
"""

email_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { 
            color: #8c060c; 
            margin-bottom: 3px; 
            text-align: center;
        }
        p { 
            color: #787777; 
            font-size: 14px;
            margin-top: 2px;  
            margin-bottom: 30px;  
            text-align: center;
        }
        .article { width: 40%; margin-bottom: 15px; }
        .article img { width: 100%; max-width: 600px; border-radius: 5px; border: 3px solid #d17dc0;}
        .article h2 { margin-top: 5px; font-size: 16px; }
        a { text-decoration: none; color: #000; }  
        a:visited { color: #000 !important; }  
        .articles h2:hover { text-decoration: underline; }
        .articles p:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>NOS {{ topic }} digest</h1>
    <p>{{ header_text }}<p>
    <div class="articles">
        {{ articles_content }}
    </div>
</body>
</html>
"""