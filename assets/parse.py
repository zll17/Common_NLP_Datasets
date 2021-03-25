import re
from bs4 import BeautifulSoup

item_lst = []

def parse_one(text):
	d2t = {}
	field = None
	nobj = re.search(r'####\s+(.+)',text)
	dataset_name = nobj.group(1)
	d2t['数据集名称'] = dataset_name
	text = re.sub(r'####\s(.+)',r'',text)
	ftxt = ''
	for line in text.split('\n'):
		obj = re.search(r'^-\s(\w+)：{0,1}',line)
		if obj!=None:
			tfield = obj.group(1)
			if field!=None:
				d2t[field] = ftxt
				field = tfield
				ftxt = ''
				if tfield.strip() in ['数据类型','用途','来源','镜像']:
					ftxt = re.search(r'[：](.*)',line).group(1).strip()
			else:
				field = tfield

			#print(field)
		else:
			line = re.sub(r'```',r'',line).strip()
			if line!='':
				ftxt += line+'\n'
	if '镜像' not in d2t:
		d2t['镜像'] = ftxt
	return d2t

html_text = '''
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="keywords" content="" />
<script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
<!-- bootstrap-css -->
<link href="css/bootstrap.css" rel="stylesheet" type="text/css" media="all" />
<!--// bootstrap-css -->
<!-- css -->
<link rel="stylesheet" href="css/style.css" type="text/css" media="all" />
<!--// css -->
<link rel="stylesheet" href="css/owl.carousel.css" type="text/css" media="all">
<link href="css/owl.theme.css" rel="stylesheet">
<link type="text/css" rel="stylesheet" href="css/cm-overlay.css" />
<!-- font-awesome icons -->
<link href="css/font-awesome.css" rel="stylesheet"> 
<!-- //font-awesome icons -->
<!-- font -->
<link href="http://fonts.googleapis.com/css?family=Roboto+Slab:100,300,400,700" rel="stylesheet">
<link href='http://fonts.googleapis.com/css?family=Roboto+Condensed:400,700italic,700,400italic,300italic,300' rel='stylesheet' type='text/css'>
<!-- //font -->
<script src="js/jquery-1.11.1.min.js"></script>
<script src="js/bootstrap.js"></script>
<!-- menu -->
<link rel="stylesheet" href="css/main.css">
<script type="text/javascript" src="js/main.js"></script>
<!-- //menu --> 
</head>
<body>

	<!-- banner -->
	<div class="banner" id="home">
'''

def to_html(dt):
	data_sample = dt['数据样例']
	data_sample = re.sub(r'\n',r'<br/>',data_sample)
	dir_structure = dt['文件结构']
	dir_structure = re.sub(r'\n',r'<br/>',dir_structure)
	dataset_name = dt['数据集名称']
	data_type = dt['数据类型']
	useness = dt['用途']
	source = dt['来源']
	mirror = dt['镜像']
	source_t = re.search(r'\[(.*?)\]',source).group(1)
	source_h = re.search(r'\((.*?)\)',source).group(1)
	mirror_t = re.search(r'\[(.*?)\]',mirror).group(1)
	mirror_h = re.search(r'\((.*?)\)',mirror).group(1)
	if re.search(r'imgs',data_sample)!=None:
		data_sample = re.search(r'\((.*?)\)',data_sample).group(1)
		data_sample = f'<img src="{data_sample}"></img>'
	
	item_txt = f'''
	<!-- banner -->
		<div class="banner" id="home">
		<div class="container">
			<div class="w3l-banner-grids">
					<div class="col-md-8 w3ls-banner-right">
						<div class="banner-right-img" style="height: 350px;">
							<div style="width:100%;height:100%;white-space: nowrap;overflow-x:auto;overflow-y:auto;color:#ffffff">
								数据样例：<br/>
								<pre>{data_sample}	</pre>
							</div>
						</div>
						<div class="banner-right-info" style="height: 350px;">
						<div style="white-space: nowrap;width:100%;height:100%;overflow-x:auto;overflow-y:auto;color:#ffffff">
								文件结构：<br/>
								<pre>{dir_structure}</pre>

						</div>
						</div>
						<div class="clearfix"> </div>
					</div>
					<div class="col-md-4 w3ls-banner-left">
						<div class="w3ls-banner-left-info">
                        	<p>数据集名称：<b style="color: #ffc300;">{dataset_name}</b></p>
						</div>
						<div class="w3ls-banner-left-info">
							<p>数据类型：{data_type}</p>
							<p>用途：{useness} </p>
						</div>
						<div class="w3ls-banner-left-info">
                        	<p>来源：<a href="{source_h}">{source_t}</a></p>
                        	<p>镜像：<a href="{mirror_h}">{mirror_t}</a></p>
						</div>
					</div>
					<div class="clearfix"> </div>
			</div>
			<!-- </div>
			<div class="w3l-banner-grids"> -->
    					<div class="clearfix"> </div>
        	</div>
		</div>
	'''
	return item_txt

with open('README.md','r',encoding='utf-8') as rfp:
	sp = BeautifulSoup(rfp.read(),'lxml')
	for idx,it in enumerate(sp.find_all('details')):
		#title = it.summary.text
		#title = re.sub(r'####\s+',r'',title)
		content = it.text
		dt = parse_one(content)
		#print(f"名称：{dt['数据集名称']}: 样例：{dt['数据样例'][:10]}\t结构：{dt['文件结构'][:15]}\t类型：{dt['数据类型'][:10]}\t用途：{dt['用途'][:10]}\t来源：{dt['来源'][:10]}")
		html_text += to_html(dt)


html_text += '''
	</body>
</html>
'''

with open('dataset_display.html','w',encoding='utf-8') as wfp:
	wfp.write(html_text)