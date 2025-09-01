/**
* Template Name: Learner
* Template URL: https://bootstrapmade.com/learner-bootstrap-course-template/
* Updated: Jul 08 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /*
   * Pricing Toggle
   */

  const pricingContainers = document.querySelectorAll('.pricing-toggle-container');

  pricingContainers.forEach(function(container) {
    const pricingSwitch = container.querySelector('.pricing-toggle input[type="checkbox"]');
    const monthlyText = container.querySelector('.monthly');
    const yearlyText = container.querySelector('.yearly');

    pricingSwitch.addEventListener('change', function() {
      const pricingItems = container.querySelectorAll('.pricing-item');

      if (this.checked) {
        monthlyText.classList.remove('active');
        yearlyText.classList.add('active');
        pricingItems.forEach(item => {
          item.classList.add('yearly-active');
        });
      } else {
        monthlyText.classList.add('active');
        yearlyText.classList.remove('active');
        pricingItems.forEach(item => {
          item.classList.remove('yearly-active');
        });
      }
    });
  });

})();

// Show message likes profile updated successfully 
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

class NotificationManager {
    constructor() {
        this.notificationBell = document.getElementById('notificationBell');
        this.notificationCount = document.getElementById('notificationCount');
        this.notificationsList = document.getElementById('notificationsList');
        this.pollingInterval = null;
        this.isPolling = false;
        
        this.init();
    }
    
    init() {
        if (!this.notificationBell) return;
        
        // Load notifications when dropdown is shown
        this.notificationBell.addEventListener('show.bs.dropdown', () => {
            this.loadNotifications();
        });
        
        // Start polling for new notifications
        this.startPolling();
        
        // Load initial notifications
        this.loadNotifications();
    }
    
    async loadNotifications() {
        try {
            const response = await fetch('/notifications/get/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch notifications');
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.updateNotificationCount(data.unread_count);
                this.renderNotifications(data.notifications);
            } else {
                console.error('Error loading notifications:', data.message);
            }
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }
    
    updateNotificationCount(unreadCount) {
        if (!this.notificationCount) return;
        
        if (unreadCount > 0) {
            this.notificationCount.textContent = unreadCount > 99 ? '99+' : unreadCount;
            this.notificationCount.style.display = 'block';
            this.notificationBell.classList.add('has-notifications');
        } else {
            this.notificationCount.style.display = 'none';
            this.notificationBell.classList.remove('has-notifications');
        }
    }
    
    renderNotifications(notifications) {
        if (!this.notificationsList) return;
        
        if (notifications.length === 0) {
            this.notificationsList.innerHTML = `
                <div class="notification-empty">
                    <i class="bi bi-bell-slash"></i>
                    <p class="mb-0">No notifications</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        notifications.forEach(notification => {
            const unreadClass = notification.is_read ? '' : 'unread';
            const timeText = notification.created_at;
            
            html += `
                <div class="notification-item ${unreadClass}" onclick="notificationManager.markNotificationAsRead(${notification.id})">
                    <div class="notification-content">
                        <div class="notification-title">${this.escapeHtml(notification.title)}</div>
                        <div class="notification-message">${this.escapeHtml(notification.message)}</div>
                        <div class="notification-time">${timeText}</div>
                    </div>
                    ${!notification.is_read ? '<div class="notification-badge">!</div>' : ''}
                </div>
            `;
        });
        
        this.notificationsList.innerHTML = html;
    }
    
    async markNotificationAsRead(notificationId) {
        try {
            const response = await fetch(`/notifications/mark_read/${notificationId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to mark notification as read');
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Reload notifications to update the UI
                this.loadNotifications();
            } else {
                console.error('Error marking notification as read:', data.message);
            }
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }
    
    async markAllAsRead() {
        try {
            const response = await fetch('/notifications/mark_all_read/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to mark all notifications as read');
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Reload notifications to update the UI
                this.loadNotifications();
            } else {
                console.error('Error marking all notifications as read:', data.message);
            }
        } catch (error) {
            console.error('Error marking all notifications as read:', error);
        }
    }
    
    startPolling() {
        if (this.isPolling) return;
        
        this.isPolling = true;
        this.pollingInterval = setInterval(() => {
            this.checkForNewNotifications();
        }, 30000); // Check every 30 seconds
    }
    
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
            this.isPolling = false;
        }
    }
    
    async checkForNewNotifications() {
        try {
            const response = await fetch('/notifications/get/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            if (!response.ok) return;
            
            const data = await response.json();
            
            if (data.success) {
                const currentCount = parseInt(this.notificationCount.textContent || '0');
                if (data.unread_count > currentCount) {
                    this.updateNotificationCount(data.unread_count);
                    this.showNotificationToast('You have new notifications!');
                }
            }
        } catch (error) {
            console.error('Error checking for new notifications:', error);
        }
    }
    
    showNotificationToast(message) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = 'position-fixed top-0 end-0 p-3';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <div class="toast align-items-center text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi bi-bell me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        const toastElement = toast.querySelector('.toast');
        const bsToast = new bootstrap.Toast(toastElement);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toast);
        });
    }
    
    getCSRFToken() {
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        return tokenElement ? tokenElement.value : '';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    destroy() {
        this.stopPolling();
    }
}

// Global function for mark all as read
function markAllAsRead() {
    if (window.notificationManager) {
        window.notificationManager.markAllAsRead();
    }
}

// Initialize notification manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.notificationManager) {
        window.notificationManager.destroy();
    }
});
