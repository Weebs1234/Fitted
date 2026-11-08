// ============================================================
// Fitted CV - File Manager for getfitted.nl
// Secure, production-ready file manager interface
// ============================================================

// ========== SECURITY: XSS Prevention ==========
/**
 * Escape HTML special characters to prevent XSS
 * @param {string} text - User-provided text
 * @returns {string} - HTML-escaped text
 */
function escapeHtml(text) {
  if (text === null || text === undefined) return '';
  const div = document.createElement('div');
  div.textContent = String(text);
  return div.innerHTML;
}

/**
 * Sanitize text for safe use in innerHTML
 * @param {string} text - User-provided text
 * @returns {string} - Sanitized text
 */
function sanitize(text) {
  if (text === null || text === undefined) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/**
 * Safely set text content (prevents XSS)
 * @param {HTMLElement} element - DOM element
 * @param {string} text - Text to set
 */
function safeText(element, text) {
  if (element) {
    element.textContent = text !== null && text !== undefined ? String(text) : '';
  }
}

// ========== FILE DATA ==========
/**
 * Sample file data - in production, this would come from your backend API
 * Each file has: id, name, type (folder/file), size, date, icon
 */
const files = [
  { id: 1, name: 'blog', type: 'folder', size: '--', date: '2024-11-08 14:30', icon: '📂' },
  { id: 2, name: 'download', type: 'folder', size: '--', date: '2024-11-08 14:30', icon: '📂' },
  { id: 3, name: 'fonts', type: 'folder', size: '--', date: '2024-11-08 14:30', icon: '📂' },
  { id: 4, name: 'img', type: 'folder', size: '--', date: '2024-11-08 14:30', icon: '📂' },
  { id: 5, name: '.htaccess', type: 'file', size: '1 KB', date: '2024-11-08 14:30', icon: '📄' },
  { id: 6, name: 'apple-touch-icon.png', type: 'file', size: '8 KB', date: '2024-11-08 14:30', icon: '🖼️' },
  { id: 7, name: 'changelog.html', type: 'file', size: '4 KB', date: '2024-11-08 14:30', icon: '🌐' },
  { id: 8, name: 'favicon.ico', type: 'file', size: '1 KB', date: '2024-11-08 14:30', icon: '🖼️' },
  { id: 9, name: 'getfitted-nl.imap', type: 'file', size: '1 KB', date: '2024-11-08 14:30', icon: '📄' },
  { id: 10, name: 'index.html', type: 'file', size: '12 KB', date: '2024-11-08 14:30', icon: '🌐' },
  { id: 11, name: 'index.php', type: 'file', size: '16 KB', date: '2024-11-08 14:30', icon: '💻' },
  { id: 12, name: 'robots.txt', type: 'file', size: '1 KB', date: '2024-11-08 14:30', icon: '📄' },
  { id: 13, name: 'sitemap.xml', type: 'file', size: '2 KB', date: '2024-11-08 14:30', icon: '📄' },
  { id: 14, name: 'style.css', type: 'file', size: '8 KB', date: '2024-11-08 14:30', icon: '🎨' },
  { id: 15, name: 'upload.php', type: 'file', size: '4 KB', date: '2024-11-08 14:30', icon: '💻' }
];

// ========== STATE ==========
let selectedFiles = new Set();
let currentPath = ['Getfitted'];
let searchQuery = '';

// ========== DOM ELEMENTS ==========
const fileTableBody = document.getElementById('file-table-body');
const searchInput = document.getElementById('search-input');
const itemCountSpan = document.getElementById('item-count');

// ========== INITIALIZATION ==========
function init() {
  renderFileTable();
  updateItemCount();
  
  // Event listeners
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      renderFileTable();
    });
  }

  // Close modals on outside click
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeAllModals();
      }
    });
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Ctrl+A to select all
    if (e.ctrlKey && e.key === 'a') {
      e.preventDefault();
      selectAll();
    }
    // Delete key
    if (e.key === 'Delete' && selectedFiles.size > 0) {
      deleteSelected();
    }
    // Escape to close modals
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });
}

// ========== RENDERING ==========
function renderFileTable() {
  if (!fileTableBody) return;

  fileTableBody.innerHTML = '';

  const filteredFiles = files.filter(file => 
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  filteredFiles.forEach(file => {
    const row = document.createElement('tr');
    if (selectedFiles.has(file.id)) {
      row.classList.add('selected');
    }

    // Create checkbox
    const checkboxTd = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'file-checkbox';
    checkbox.dataset.id = file.id;
    checkbox.checked = selectedFiles.has(file.id);
    checkbox.addEventListener('change', () => toggleSelect(file.id));
    checkboxTd.appendChild(checkbox);

    // Create icon cell
    const iconTd = document.createElement('td');
    const iconSpan = document.createElement('span');
    iconSpan.className = 'file-icon';
    iconSpan.textContent = file.icon;
    iconTd.appendChild(iconSpan);

    // Create name cell with safe text
    const nameTd = document.createElement('td');
    const nameLink = document.createElement('a');
    nameLink.className = 'file-name';
    nameLink.href = '#';
    nameLink.textContent = file.name;
    nameLink.addEventListener('click', (e) => {
      e.preventDefault();
      openFile(file.id);
    });
    nameTd.appendChild(nameLink);

    // Create size cell with safe text
    const sizeTd = document.createElement('td');
    const sizeSpan = document.createElement('span');
    sizeSpan.className = 'file-size';
    safeText(sizeSpan, file.size);
    sizeTd.appendChild(sizeSpan);

    // Create date cell with safe text
    const dateTd = document.createElement('td');
    const dateSpan = document.createElement('span');
    dateSpan.className = 'file-date';
    safeText(dateSpan, file.date);
    dateTd.appendChild(dateSpan);

    // Assemble row
    row.appendChild(checkboxTd);
    row.appendChild(iconTd);
    row.appendChild(nameTd);
    row.appendChild(sizeTd);
    row.appendChild(dateTd);

    // Row click for selection
    row.addEventListener('click', (e) => {
      if (e.target.type !== 'checkbox' && e.target.tagName !== 'A') {
        toggleSelect(file.id);
      }
    });

    fileTableBody.appendChild(row);
  });

  updateItemCount();
}

// ========== SELECTION ==========
function toggleSelect(fileId) {
  if (selectedFiles.has(fileId)) {
    selectedFiles.delete(fileId);
  } else {
    selectedFiles.add(fileId);
  }
  renderFileTable();
}

function selectAll() {
  files.forEach(file => selectedFiles.add(file.id));
  renderFileTable();
}

function deselectAll() {
  selectedFiles.clear();
  renderFileTable();
}

function updateItemCount() {
  if (!itemCountSpan) return;
  const count = selectedFiles.size;
  itemCountSpan.textContent = `${count} ${count === 1 ? 'item' : 'items'} geselecteerd`;
}

// ========== FILE OPERATIONS ==========
function openFile(fileId) {
  const file = files.find(f => f.id === fileId);
  if (!file) return;

  if (file.type === 'folder') {
    // Navigate into folder - in production, load folder contents from server
    showToast(`Map: ${sanitize(file.name)}`, 'info');
  } else {
    // Open file - in production, download or view the file
    showToast(`Bestand: ${sanitize(file.name)}`, 'info');
  }
}

// ========== MODALS ==========
function showUploadModal() {
  closeAllModals();
  document.getElementById('uploadModal').classList.add('active');
}

function closeUploadModal() {
  document.getElementById('uploadModal').classList.remove('active');
  document.getElementById('file-upload').value = '';
}

function showNewFolderModal() {
  closeAllModals();
  document.getElementById('newFolderModal').classList.add('active');
  document.getElementById('folder-name').focus();
}

function closeNewFolderModal() {
  document.getElementById('newFolderModal').classList.remove('active');
  document.getElementById('folder-name').value = '';
}

function showMoreMenu() {
  closeAllModals();
  document.getElementById('moreMenuModal').classList.add('active');
}

function closeMoreMenu() {
  document.getElementById('moreMenuModal').classList.remove('active');
}

function closeAllModals() {
  document.querySelectorAll('.modal').forEach(modal => {
    modal.classList.remove('active');
  });
}

// ========== ACTIONS ==========
function uploadFiles() {
  const input = document.getElementById('file-upload');
  if (input.files.length > 0) {
    // In production, upload to server via AJAX
    showToast(`Uploading ${input.files.length} file(s)`, 'success');
    closeUploadModal();
    
    // Simulate adding uploaded files
    Array.from(input.files).forEach((file, index) => {
      files.unshift({
        id: files.length + index + 1,
        name: sanitize(file.name),
        type: 'file',
        size: formatFileSize(file.size),
        date: new Date().toLocaleString('nl-NL', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        icon: getFileIcon(file.name)
      });
    });
    
    renderFileTable();
  }
}

function createFolder() {
  const folderName = document.getElementById('folder-name').value.trim();
  if (folderName) {
    // In production, create folder on server via AJAX
    files.unshift({
      id: files.length + 1,
      name: sanitize(folderName),
      type: 'folder',
      size: '--',
      date: new Date().toLocaleString('nl-NL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }),
      icon: '📂'
    });
    
    renderFileTable();
    closeNewFolderModal();
    showToast(`Map '${sanitize(folderName)}' gemaakt`, 'success');
  }
}

function deleteSelected() {
  if (selectedFiles.size > 0) {
    if (confirm(`Weet u zeker dat u ${selectedFiles.size} geselecteerde ${selectedFiles.size === 1 ? 'item' : 'items'} wilt verwijderen?`)) {
      // In production, delete on server via AJAX
      const newFiles = files.filter(file => !selectedFiles.has(file.id));
      files.length = 0;
      files.push(...newFiles);
      selectedFiles.clear();
      renderFileTable();
      showToast(`${selectedFiles.size} items verwijderd`, 'success');
    }
  }
}

function refreshView() {
  // In production, reload from server
  renderFileTable();
  showToast('Vernieuwd', 'info');
}

// ========== TOAST NOTIFICATIONS ==========
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  if (toast) {
    toast.textContent = sanitize(message);
    toast.className = 'toast show ' + type;
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
      toast.classList.remove('show', type);
    }, 3000);
  }
}

// ========== UTILITY FUNCTIONS ==========
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function getFileIcon(filename) {
  const extension = filename.split('.').pop().toLowerCase();
  const icons = {
    folder: '📂',
    png: '🖼️',
    jpg: '🖼️',
    jpeg: '🖼️',
    gif: '🖼️',
    svg: '🖼️',
    html: '🌐',
    css: '🎨',
    js: '💻',
    php: '💻',
    txt: '📄',
    md: '📄',
    pdf: '📄',
    doc: '📄',
    docx: '📄',
    xls: '📊',
    xlsx: '📊',
    ppt: '📑',
    pptx: '📑',
    zip: '🗄️',
    rar: '🗄️',
    ico: '🖼️',
    imap: '📧',
    xml: '📄'
  };
  return icons[extension] || '📄';
}

// ========== INITIALIZE ==========
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
