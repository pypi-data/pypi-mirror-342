() => {
    const interactiveElements = document.querySelectorAll('button, input, select, textarea, a[href], [onclick], [role="button"]');
    let count = 1;
    const markContainer = document.createElement('div');
    markContainer.style.position = 'absolute';
    markContainer.style.top = '0';
    markContainer.style.left = '0';
    markContainer.style.width = '100%';
    markContainer.style.height = '100%';
    markContainer.style.pointerEvents = 'none';
    markContainer.style.zIndex = '9999';
    document.body.appendChild(markContainer);
    
    interactiveElements.forEach(element => {
        const rect = element.getBoundingClientRect();
        const highlightDiv = document.createElement('div');
        highlightDiv.className = 'interactive-highlight';
        highlightDiv.style.position = 'absolute';
        highlightDiv.style.top = `${rect.top + window.scrollY}px`;
        highlightDiv.style.left = `${rect.left + window.scrollX}px`;
        highlightDiv.style.width = `${rect.width}px`;
        highlightDiv.style.height = `${rect.height}px`;
        
        const numberDiv = document.createElement('div');
        numberDiv.className = 'element-number';
        numberDiv.textContent = count;
        highlightDiv.appendChild(numberDiv);
        markContainer.appendChild(highlightDiv);
        count++;
    });
    
    return count - 1;
}