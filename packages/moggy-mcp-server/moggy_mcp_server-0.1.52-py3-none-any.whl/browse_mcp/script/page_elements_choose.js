() => {
    const elements = document.querySelectorAll('.interactive-highlight');
    
    // 构建网站基本信息
    const siteInfo = {
        title: document.title,
        url: window.location.href,
        domain: window.location.hostname,
        path: window.location.pathname,
        timestamp: new Date().toISOString(),
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight
        },
        meta: {
            description: document.querySelector('meta[name="description"]')?.content || '',
            keywords: document.querySelector('meta[name="keywords"]')?.content || ''
        }
    };

    const selectedElements = [];
    
    elements.forEach((element, index) => {
        // 获取元素基本信息
        const rect = element.getBoundingClientRect();
        const tagName = element.tagName.toLowerCase();
        
        // 获取元素文本内容
        let text = element.textContent?.trim() || '';
        if (text.length > 100) {
            text = text.substring(0, 100) + '...';
        }
        
        // 获取元素href属性(如果存在)
        const href = element.getAttribute('href') || '';
        
        // 构建元素说明
        let description = text || href || tagName;
        
        // 构建Playwright选择器
        let selector = tagName;
        if (element.id) {
            selector = `#${element.id}`;
        } else if (text) {
            // 移除文本中的特殊字符
            const cleanText = text.replace(/[\s\n\r\t]+/g, ' ').trim();
            selector = `text=${cleanText}`;
        } else if (element.className) {
            // 移除类名中的特殊字符
            const cleanClassName = element.className.replace(/[\s\n\r\t]+/g, ' ').trim();
            selector = `.${cleanClassName.split(' ').join('.')}`;
        }
        
        selectedElements.push({
            number: index + 1,
            name: tagName,
            location: {
                x: Math.round(rect.x),
                y: Math.round(rect.y),
                width: Math.round(rect.width),
                height: Math.round(rect.height)
            },
            href: href,
            text: text,
            description: description,
            selector: selector
        });
    });
    
    // 构建最终返回对象
    const result = {
        siteInfo: siteInfo,
        selectedElements: selectedElements
    };
    
    return JSON.stringify(result, null, 2);
}