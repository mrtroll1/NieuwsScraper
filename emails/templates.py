article_template = """
<div style="margin-bottom: 15px; padding: 5px; border: 0; border-radius: 5px; text-align: center; max-width: 50%; margin: 0 auto;">
    <a href="{{ url }}" style="text-decoration: none; color: #000;">
        <h2 style="margin-top: 10px; font-size: 16px; text-align: center; max-width: 70%; margin: 0 auto; word-wrap: break-word;">{{ title }}</h2>
        <img src="{{ photo_url }}" alt="{{ title }}" style="width: 100%; max-width: 400px; border-radius: 5px; border: 3px solid #d17dc0; display: block; margin: 0 auto; margin-bottom: 10px;"/>
        <p style="text-align: center; max-width: 70%; margin: 0 auto; margin-bottom: 30px !important; word-wrap: break-word;">{{ description }}</p>

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
            margin-bottom: 3px; /* Reduce space below the h1 */
            text-align: center;
        }
        p { 
            color: #787777; 
            font-size: 14px;
            margin-top: 2px;  /* Reduce space above the p */
            margin-bottom: 30px;  /* Optional: control space below the p */
            text-align: center;
        }
        .article { width: 40%; margin-bottom: 15px; }
        .article img { width: 100%; max-width: 600px; border-radius: 5px; border: 3px solid #d17dc0;}
        .article h2 { margin-top: 5px; font-size: 16px; }
        a { text-decoration: none; color: #000; }  /* Ensure all links are black */
        a:visited { color: #000 !important; }  /* Override visited link color */
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