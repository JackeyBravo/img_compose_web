class ImageCompressor {
    constructor() {
        this.initElements();
        this.initEventListeners();
        this.currentFile = null;
    }

    initElements() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.previewArea = document.getElementById('previewArea');
        this.originalImage = document.getElementById('originalImage');
        this.compressedImage = document.getElementById('compressedImage');
        this.originalSize = document.getElementById('originalSize');
        this.compressedSize = document.getElementById('compressedSize');
        this.qualitySlider = document.getElementById('quality');
        this.qualityValue = document.getElementById('qualityValue');
        this.downloadBtn = document.getElementById('downloadBtn');
    }

    initEventListeners() {
        // 拖拽上传
        this.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.dropZone.style.borderColor = '#007AFF';
        });

        this.dropZone.addEventListener('dragleave', () => {
            this.dropZone.style.borderColor = '#DEDEDE';
        });

        this.dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.dropZone.style.borderColor = '#DEDEDE';
            const files = e.dataTransfer.files;
            if (files.length) this.handleFile(files[0]);
        });

        // 点击上传
        this.dropZone.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) this.handleFile(e.target.files[0]);
        });

        // 质量调节
        this.qualitySlider.addEventListener('input', (e) => {
            this.qualityValue.textContent = `${e.target.value}%`;
            if (this.currentFile) this.compressImage(this.currentFile);
        });

        // 下载按钮
        this.downloadBtn.addEventListener('click', () => this.downloadImage());
    }

    handleFile(file) {
        if (!file.type.match('image.*')) {
            alert('请上传图片文件！');
            return;
        }

        this.currentFile = file;
        this.previewArea.hidden = false;
        this.originalSize.textContent = this.formatFileSize(file.size);

        const reader = new FileReader();
        reader.onload = (e) => {
            this.originalImage.src = e.target.result;
            this.compressImage(file);
        };
        reader.readAsDataURL(file);
    }

    compressImage(file) {
        const quality = this.qualitySlider.value / 100;
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);

                canvas.toBlob((blob) => {
                    this.compressedImage.src = URL.createObjectURL(blob);
                    this.compressedSize.textContent = this.formatFileSize(blob.size);
                }, file.type, quality);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    downloadImage() {
        const link = document.createElement('a');
        link.download = `compressed_${this.currentFile.name}`;
        link.href = this.compressedImage.src;
        link.click();
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// 初始化应用
new ImageCompressor(); 