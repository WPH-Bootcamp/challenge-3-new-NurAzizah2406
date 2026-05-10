import re

with open('src/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add inline script to head
head_script = """  <script>
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark')
    }
  </script>
</head>"""
content = content.replace("</head>", head_script)

# Body bg
content = content.replace('body class="bg-neutral-950 text-white', 'body class="bg-white text-neutral-900 dark:bg-neutral-950 dark:text-white')

# General replacements
# text-white -> text-neutral-900 dark:text-white
# text-neutral-300 -> text-neutral-600 dark:text-neutral-300
# text-neutral-400 -> text-neutral-500 dark:text-neutral-400
# bg-neutral-900 -> bg-neutral-50 dark:bg-neutral-900
# bg-neutral-950 -> bg-white dark:bg-neutral-950
# border-neutral-800 -> border-neutral-200 dark:border-neutral-800

# Function to safely replace classes inside class="..." strings
def replace_in_classes(match):
    cls_str = match.group(1)
    
    # We do NOT replace text-white if bg-brand is in the same class list
    # or if it's the CTA Let's talk it through
    if "bg-brand" not in cls_str and "text-[80px]" not in cls_str:
        cls_str = re.sub(r'\btext-white\b', 'text-neutral-900 dark:text-white', cls_str)
    
    # Replace other classes
    cls_str = re.sub(r'\btext-neutral-300\b', 'text-neutral-600 dark:text-neutral-300', cls_str)
    cls_str = re.sub(r'\btext-neutral-400\b', 'text-neutral-500 dark:text-neutral-400', cls_str)
    cls_str = re.sub(r'\bbg-neutral-900\b', 'bg-neutral-50 dark:bg-neutral-900', cls_str)
    cls_str = re.sub(r'\bbg-neutral-950\b', 'bg-white dark:bg-neutral-950', cls_str)
    cls_str = re.sub(r'\bborder-neutral-800\b', 'border-neutral-200 dark:border-neutral-800', cls_str)
    
    return f'class="{cls_str}"'

content = re.sub(r'class="([^"]+)"', replace_in_classes, content)

# Navbar toggle button
toggle_button_html = """      <!-- Theme Toggle -->
      <button id="theme-toggle" class="p-2 ml-4 rounded-full bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 focus:outline-none transition-colors border border-neutral-200 dark:border-neutral-700">
        <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
        <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 4.22a1 1 0 011.415 0l.708.708a1 1 0 01-1.414 1.414l-.708-.708a1 1 0 010-1.414zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM14.5 14.5a1 1 0 010 1.415l-.708.708a1 1 0 01-1.414-1.414l.708-.708a1 1 0 011.414 0zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm-4.22-4.22a1 1 0 010-1.415l-.708-.708a1 1 0 01-1.414 1.414l.708.708a1 1 0 011.414 0zM2 10a1 1 0 011-1h1a1 1 0 110 2H3a1 1 0 01-1-1zm3.28-6.72a1 1 0 010 1.415l-.708.708a1 1 0 01-1.414-1.414l.708-.708a1 1 0 011.414 0zM10 5a5 5 0 100 10 5 5 0 000-10z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
      </button>
      <!-- Mobile Menu Toggle -->"""

content = content.replace("<!-- Mobile Menu Toggle -->", toggle_button_html)

# Toggle JS script
js_script = """    // Theme Toggle Logic
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const themeToggleBtn = document.getElementById('theme-toggle');

    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        themeToggleLightIcon.classList.remove('hidden');
    } else {
        themeToggleDarkIcon.classList.remove('hidden');
    }

    themeToggleBtn?.addEventListener('click', function() {
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    });

    // Form Success Modal Logic"""

content = content.replace("// Form Success Modal Logic", js_script)

with open('src/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
