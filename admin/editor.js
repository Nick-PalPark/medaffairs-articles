/**
 * MedAffairs Articles Editor JavaScript
 * Provides functionality to view and edit article manual titles
 */

class ArticleEditor {
    constructor() {
        this.articles = [];
        this.filteredArticles = [];
        this.currentFilter = 'all';
        this.searchTerm = '';
        this.articlesData = null;
        this.hasChanges = false;
        
        this.init();
    }
    
    async init() {
        await this.loadArticles();
        this.setupEventListeners();
        this.updateDisplay();
    }
    
    async loadArticles() {
        try {
            // Try to load articles.json from the parent directory
            const response = await fetch('../articles.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.articlesData = await response.json();
            this.articles = this.articlesData.articles || [];
            this.filteredArticles = [...this.articles];
            
            document.getElementById('loadingArea').style.display = 'none';
            document.getElementById('articlesContainer').style.display = 'grid';
            
        } catch (error) {
            console.error('Error loading articles:', error);
            this.showMessage('Error loading articles. Make sure articles.json exists in the parent directory.', 'error');
            document.getElementById('loadingArea').innerHTML = 'Error loading articles';
        }
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.applyFilters();
        });
        
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.applyFilters();
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 's':
                        e.preventDefault();
                        this.saveChanges();
                        break;
                    case 'f':
                        e.preventDefault();
                        document.getElementById('searchInput').focus();
                        break;
                }
            }
        });
        
        // Warn about unsaved changes
        window.addEventListener('beforeunload', (e) => {
            if (this.hasChanges) {
                e.preventDefault();
                e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
            }
        });
    }
    
    applyFilters() {
        this.filteredArticles = this.articles.filter(article => {
            // Apply search filter
            if (this.searchTerm) {
                const searchFields = [
                    article.title,
                    article.manual_title,
                    article.content,
                    article.source,
                    article.tags?.join(' ')
                ].filter(Boolean).join(' ').toLowerCase();
                
                if (!searchFields.includes(this.searchTerm)) {
                    return false;
                }
            }
            
            // Apply category filter
            switch (this.currentFilter) {
                case 'heroes':
                    return article.is_hero;
                case 'columns':
                    return article.is_column;
                case 'manual':
                    return article.manual_title && article.manual_title.trim() !== '';
                case 'recent':
                    const weekAgo = new Date();
                    weekAgo.setDate(weekAgo.getDate() - 7);
                    return new Date(article.published_date) > weekAgo;
                default:
                    return true;
            }
        });
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        this.updateStats();
        this.renderArticles();
    }
    
    updateStats() {
        const heroCount = this.articles.filter(a => a.is_hero).length;
        const columnCount = this.articles.filter(a => a.is_column).length;
        const manualTitleCount = this.articles.filter(a => a.manual_title && a.manual_title.trim()).length;
        
        document.getElementById('totalArticles').textContent = this.articles.length;
        document.getElementById('heroCount').textContent = heroCount;
        document.getElementById('columnCount').textContent = columnCount;
        document.getElementById('manualTitles').textContent = manualTitleCount;
        
        // Update last updated time
        if (this.articlesData?.last_updated) {
            const lastUpdated = new Date(this.articlesData.last_updated);
            document.getElementById('lastUpdated').textContent = lastUpdated.toLocaleString();
        }
    }
    
    renderArticles() {
        const container = document.getElementById('articlesContainer');
        
        if (this.filteredArticles.length === 0) {
            container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #666;">No articles found matching your criteria.</div>';
            return;
        }
        
        container.innerHTML = this.filteredArticles.map(article => this.renderArticle(article)).join('');
        
        // Add event listeners to the newly created elements
        this.attachArticleEventListeners();
    }
    
    renderArticle(article) {
        const publishedDate = new Date(article.published_date).toLocaleDateString();
        const badges = [];
        
        if (article.is_hero) badges.push('<span class="badge badge-hero">Hero</span>');
        if (article.is_column) badges.push('<span class="badge badge-column">Column</span>');
        
        article.tags?.forEach(tag => {
            badges.push(`<span class="badge badge-tag">${tag}</span>`);
        });
        
        const displayTitle = article.manual_title || article.title;
        const hasManualTitle = article.manual_title && article.manual_title.trim() !== '';
        
        return `
            <div class="article-card" data-id="${article.id}">
                <div class="article-header">
                    <div style="flex: 1;">
                        <div class="article-title">${this.escapeHtml(displayTitle)}</div>
                        <div class="article-meta">
                            Published: ${publishedDate} | Source: ${this.escapeHtml(article.source)}
                        </div>
                    </div>
                </div>
                
                <div class="article-badges">
                    ${badges.join('')}
                </div>
                
                <div class="manual-title-section">
                    <label class="manual-title-label">Manual Title Override:</label>
                    <input 
                        type="text" 
                        class="manual-title-input" 
                        data-article-id="${article.id}"
                        value="${this.escapeHtml(article.manual_title || '')}"
                        placeholder="${this.escapeHtml(article.title)}"
                        ${hasManualTitle ? 'style="border-color: #27ae60; background-color: #f8fff8;"' : ''}
                    >
                </div>
                
                <div class="article-summary">
                    ${this.escapeHtml(this.truncateText(article.summary || article.content, 150))}
                </div>
                
                <div class="article-actions">
                    <a href="${article.url}" target="_blank" class="btn btn-primary">View Original</a>
                    <button class="btn ${article.is_hero ? 'btn-danger' : 'btn-secondary'}" onclick="editor.toggleHero('${article.id}')">
                        ${article.is_hero ? 'Remove Hero' : 'Make Hero'}
                    </button>
                    <button class="btn ${article.is_column ? 'btn-danger' : 'btn-secondary'}" onclick="editor.toggleColumn('${article.id}')">
                        ${article.is_column ? 'Remove Column' : 'Make Column'}
                    </button>
                    ${hasManualTitle ? '<button class="btn btn-danger" onclick="editor.clearManualTitle(\'' + article.id + '\')">Clear Manual Title</button>' : ''}
                </div>
            </div>
        `;
    }
    
    attachArticleEventListeners() {
        // Manual title inputs
        document.querySelectorAll('.manual-title-input').forEach(input => {
            input.addEventListener('input', (e) => {
                const articleId = e.target.dataset.articleId;
                const value = e.target.value.trim();
                this.updateManualTitle(articleId, value);
                
                // Update visual feedback
                if (value) {
                    e.target.style.borderColor = '#27ae60';
                    e.target.style.backgroundColor = '#f8fff8';
                } else {
                    e.target.style.borderColor = '#ddd';
                    e.target.style.backgroundColor = 'white';
                }
            });
        });
    }
    
    updateManualTitle(articleId, title) {
        const article = this.articles.find(a => a.id === articleId);
        if (article) {
            article.manual_title = title || null;
            this.hasChanges = true;
            this.showSaveButton();
        }
    }
    
    toggleHero(articleId) {
        const article = this.articles.find(a => a.id === articleId);
        if (!article) return;
        
        if (article.is_hero) {
            article.is_hero = false;
        } else {
            // Check hero limit
            const heroCount = this.articles.filter(a => a.is_hero).length;
            const maxHeroes = this.articlesData?.limits?.max_heroes || 3;
            
            if (heroCount >= maxHeroes) {
                this.showMessage(`Cannot exceed limit of ${maxHeroes} heroes. Remove another hero first.`, 'error');
                return;
            }
            
            article.is_hero = true;
            // Remove from columns if it was a column
            if (article.is_column) {
                article.is_column = false;
            }
        }
        
        this.hasChanges = true;
        this.updateDisplay();
        this.showSaveButton();
    }
    
    toggleColumn(articleId) {
        const article = this.articles.find(a => a.id === articleId);
        if (!article) return;
        
        if (article.is_column) {
            article.is_column = false;
        } else {
            // Check column limit
            const columnCount = this.articles.filter(a => a.is_column).length;
            const maxColumns = this.articlesData?.limits?.max_columns || 6;
            
            if (columnCount >= maxColumns) {
                this.showMessage(`Cannot exceed limit of ${maxColumns} columns. Remove another column first.`, 'error');
                return;
            }
            
            article.is_column = true;
            // Remove from heroes if it was a hero
            if (article.is_hero) {
                article.is_hero = false;
            }
        }
        
        this.hasChanges = true;
        this.updateDisplay();
        this.showSaveButton();
    }
    
    clearManualTitle(articleId) {
        const article = this.articles.find(a => a.id === articleId);
        if (article) {
            article.manual_title = null;
            this.hasChanges = true;
            this.updateDisplay();
            this.showSaveButton();
        }
    }
    
    showSaveButton() {
        if (!document.getElementById('saveButton')) {
            const saveButton = document.createElement('div');
            saveButton.id = 'saveButton';
            saveButton.innerHTML = `
                <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
                    <button class="btn btn-success" onclick="editor.saveChanges()" style="padding: 12px 24px; font-size: 16px;">
                        Save Changes (Ctrl+S)
                    </button>
                </div>
            `;
            document.body.appendChild(saveButton);
        }
    }
    
    async saveChanges() {
        try {
            // Update the articles data structure
            this.articlesData.articles = this.articles;
            this.articlesData.heroes = this.articles.filter(a => a.is_hero).map(a => a.id);
            this.articlesData.columns = this.articles.filter(a => a.is_column).map(a => a.id);
            this.articlesData.last_updated = new Date().toISOString();
            
            // Create download link for the updated JSON
            const dataStr = JSON.stringify(this.articlesData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'articles.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.hasChanges = false;
            this.removeSaveButton();
            this.showMessage('Changes saved! Download the articles.json file and commit it to the repository.', 'success');
            
        } catch (error) {
            console.error('Error saving changes:', error);
            this.showMessage('Error saving changes: ' + error.message, 'error');
        }
    }
    
    removeSaveButton() {
        const saveButton = document.getElementById('saveButton');
        if (saveButton) {
            saveButton.remove();
        }
    }
    
    showMessage(message, type = 'info') {
        const messageArea = document.getElementById('messageArea');
        const messageEl = document.createElement('div');
        messageEl.className = type;
        messageEl.textContent = message;
        
        messageArea.appendChild(messageEl);
        
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 5000);
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    truncateText(text, maxLength) {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
}

// Initialize the editor when the page loads
let editor;
document.addEventListener('DOMContentLoaded', () => {
    editor = new ArticleEditor();
});