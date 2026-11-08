# Getfitted.nl Website Files

This package contains the files for your **file manager interface** and **FITTED CV logos** to upload to your webspace at getfitted.nl.

## 📁 Files Included

| File | Description | Size |
|------|-------------|------|
| `index.html` | Main file manager interface | 5.5 KB |
| `styles.css` | Dark theme stylesheet | 8.7 KB |
| `script.js` | Full functionality (upload, delete, search, etc.) | 12 KB |
| `logo-fitted-cv-light.svg` | FITTED CV logo (white background) | 0.9 KB |
| `logo-fitted-cv-dark.svg` | FITTED CV logo (black background) | 0.9 KB |

## ✨ Features

### File Manager
- ✅ Dark theme matching your screenshot
- ✅ Storage progress bar (20.41 MB / 100 MB)
- ✅ File table with checkboxes, icons, sizes, dates
- ✅ Search functionality
- ✅ Upload files (drag & drop or file picker)
- ✅ Create new folders
- ✅ Delete selected files
- ✅ Multi-select with Ctrl+A
- ✅ Keyboard shortcuts (Delete, Escape)
- ✅ Toast notifications
- ✅ Responsive design (works on mobile/tablet)

### Security
- ✅ **XSS Protection**: All user content is properly escaped
- ✅ **Input Sanitization**: Prevents malicious code injection
- ✅ **Safe DOM manipulation**: Uses textContent instead of innerHTML where appropriate

### FITTED CV Logos
- ✅ Light mode version (white background)
- ✅ Dark mode version (black background)
- ✅ SVG format (scalable, small file size)
- ✅ Professional design with document icon

## 🚀 How to Upload

### Option 1: Via FTP
1. Connect to your webspace via FTP (e.g., FileZilla)
2. Navigate to your website root (usually `/public_html/` or `/htdocs/`)
3. Upload all files from this folder
4. The file manager will be accessible at: `https://getfitted.nl/`

### Option 2: Via Control Panel
1. Log in to your hosting control panel (cPanel, DirectAdmin, Plesk, etc.)
2. Go to **File Manager**
3. Navigate to your website root
4. Upload all files
5. The file manager will be accessible at your domain

### Option 3: Via SSH
```bash
# Connect to your server
ssh yourusername@yourserver.com

# Navigate to website root
cd /path/to/your/website

# Upload files (using SCP from your local machine)
scp -r getfitted-website/* yourusername@yourserver.com:/path/to/your/website/
```

## 🔧 Configuration

### Update Storage Information
In `index.html`, find and update the storage display:
```html
<span>20,41 MB van 100 MB in gebruik</span>
<div class="progress-container">
    <div class="progress-bar" style="width: 20.41%"></div>
</div>
```

To connect to your actual storage API, you'll need to:
1. Replace the static files array in `script.js` with an API call
2. Update the upload/delete functions to call your backend

### Connect to Backend API
Currently, the file manager uses a static list of files. To connect to your actual backend:

**In `script.js`, replace the `files` array with:**
```javascript
// Fetch files from your API
async function loadFiles() {
  try {
    const response = await fetch('/api/files');
    return await response.json();
  } catch (error) {
    console.error('Failed to load files:', error);
    return [];
  }
}
```

**Update upload function:**
```javascript
async function uploadFiles() {
  const input = document.getElementById('file-upload');
  if (input.files.length > 0) {
    const formData = new FormData();
    Array.from(input.files).forEach(file => {
      formData.append('files[]', file);
    });
    
    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        showToast('Files uploaded successfully', 'success');
        closeUploadModal();
        loadFiles().then(data => {
          // Update files and re-render
        });
      } else {
        showToast('Upload failed', 'error');
      }
    } catch (error) {
      showToast('Error: ' + error.message, 'error');
    }
  }
}
```

## 🎨 Customization

### Change Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --bg-primary: #0a0a0a;      /* Dark background */
    --bg-secondary: #1a1a1a;    /* Slightly lighter */
    --bg-tertiary: #2a2a2a;     /* Even lighter */
    --text-primary: #ffffff;   /* White text */
    --text-secondary: #b0b0b0; /* Light gray text */
    --accent-blue: #0078d4;    /* Blue accent */
    --accent-blue-hover: #005a9e; /* Blue hover */
}
```

### Change Language
The interface is currently in Dutch. To change to English:
1. Update all Dutch text in `index.html`
2. Update messages in `script.js`

### Add More File Types
In `script.js`, update the `getFileIcon` function:
```javascript
function getFileIcon(filename) {
  const extension = filename.split('.').pop().toLowerCase();
  const icons = {
    folder: '📂',
    png: '🖼️',
    jpg: '🖼️',
    // Add more extensions here
    docx: '📄',
    xlsx: '📊',
    // ...
  };
  return icons[extension] || '📄';
}
```

## 📱 Responsive Design

The file manager is fully responsive and works on:
- Desktop (recommended: 1200px+)
- Tablet (768px - 1024px)
- Mobile (480px - 767px)
- Small mobile (< 480px)

## 🔒 Security Notes

✅ **XSS Protection**: All user-provided content is properly escaped using `sanitize()` and `escapeHtml()` functions

✅ **Safe DOM Manipulation**: Uses `textContent` instead of `innerHTML` for user content

✅ **Input Validation**: File names and user input are sanitized before display

⚠️ **Important**: When connecting to a backend API, ensure your API also validates and sanitizes all inputs to prevent security vulnerabilities.

## 🎯 Next Steps

1. ✅ Download the ZIP file
2. ✅ Upload to your webspace
3. ⏳ Connect to your backend API (if you have one)
4. ⏳ Customize colors and branding
5. ⏳ Test on different devices

## 📞 Support

Need help with:
- Uploading files?
- Connecting to your backend?
- Customizing the design?
- Adding features?

Just ask!

## 📄 License

These files are provided as-is for your use on getfitted.nl. You are free to modify and use them as needed.

---

**Created:** November 8, 2026  
**Version:** 1.0  
**For:** getfitted.nl
