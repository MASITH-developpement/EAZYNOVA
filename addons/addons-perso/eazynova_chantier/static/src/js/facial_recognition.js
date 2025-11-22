/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";

/**
 * Composant de capture pour la reconnaissance faciale
 * Permet de capturer une image via webcam pour l'authentification
 */
export class FacialRecognitionCapture extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        
        this.videoRef = useRef("video");
        this.canvasRef = useRef("canvas");
        
        this.state = useState({
            streaming: false,
            captured: false,
            processing: false,
            imageData: null,
        });
        
        this.stream = null;
        
        onMounted(() => {
            this.startCamera();
        });
        
        onWillUnmount(() => {
            this.stopCamera();
        });
    }
    
    /**
     * Démarre la caméra
     */
    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user"
                },
                audio: false
            });
            
            const video = this.videoRef.el;
            if (video) {
                video.srcObject = this.stream;
                video.play();
                this.state.streaming = true;
            }
        } catch (error) {
            console.error("Erreur accès caméra:", error);
            this.notification.add("Impossible d'accéder à la caméra. Vérifiez les permissions.", {
                type: "danger",
            });
        }
    }
    
    /**
     * Arrête la caméra
     */
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.state.streaming = false;
        }
    }
    
    /**
     * Capture une image depuis la webcam
     */
    captureImage() {
        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        
        if (!video || !canvas) return;
        
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Conversion en base64
        this.state.imageData = canvas.toDataURL('image/jpeg', 0.9);
        this.state.captured = true;
        
        this.stopCamera();
    }
    
    /**
     * Recommence la capture
     */
    retake() {
        this.state.captured = false;
        this.state.imageData = null;
        this.startCamera();
    }
    
    /**
     * Envoie l'image pour authentification
     */
    async authenticate() {
        if (!this.state.imageData) return;
        
        this.state.processing = true;
        
        try {
            const result = await this.rpc('/eazynova/facial/authenticate', {
                image_data: this.state.imageData.split(',')[1], // Enlever le préfixe data:image
                db: this.env.services.rpc.db
            });
            
            if (result.success) {
                this.notification.add(`Bienvenue ${result.name} !`, {
                    title: "Authentification réussie",
                    type: "success",
                });
                
                // Redirection vers le dashboard
                window.location.href = '/web';
            } else {
                this.notification.add(result.error || "Reconnaissance faciale échouée", {
                    type: "danger",
                });
                this.retake();
            }
        } catch (error) {
            console.error("Erreur authentification:", error);
            this.notification.add("Erreur lors de l'authentification", {
                type: "danger",
            });
            this.retake();
        } finally {
            this.state.processing = false;
        }
    }
}

FacialRecognitionCapture.template = "eazynova.FacialRecognitionCapture";

registry.category("actions").add("eazynova.facial_recognition", FacialRecognitionCapture);