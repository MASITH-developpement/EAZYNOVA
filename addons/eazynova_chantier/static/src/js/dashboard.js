/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

/**
 * Composant Dashboard EAZYNOVA
 * Tableau de bord interactif avec statistiques en temps réel
 */
export class EazynovaDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.notification = useService("notification");
        
        this.state = useState({
            data: null,
            loading: true,
            error: null,
        });
        
        onWillStart(async () => {
            await this.loadData();
        });
    }
    
    /**
     * Charge les données du dashboard
     */
    async loadData() {
        try {
            this.state.loading = true;
            const result = await this.rpc('/eazynova/dashboard/data');
            
            if (result.success) {
                this.state.data = result.data;
            } else {
                this.state.error = result.error;
            }
        } catch (error) {
            console.error('Erreur chargement dashboard:', error);
            this.state.error = "Erreur de chargement des données";
        } finally {
            this.state.loading = false;
        }
    }
    
    /**
     * Ouvre l'assistant IA
     */
    async openAiAssistant() {
        const query = prompt("Posez votre question à l'assistant IA:");
        
        if (!query) return;
        
        try {
            const result = await this.rpc('/eazynova/ai/assist', {
                query: query,
                context: {
                    model: 'dashboard',
                    company_id: this.state.data.company.id,
                }
            });
            
            if (result.success) {
                this.notification.add(result.response, {
                    title: "Assistant IA",
                    type: "info",
                });
            } else {
                this.notification.add(result.error, {
                    title: "Erreur",
                    type: "danger",
                });
            }
        } catch (error) {
            console.error('Erreur IA:', error);
            this.notification.add("Erreur lors de la communication avec l'IA", {
                type: "danger",
            });
        }
    }
    
    /**
     * Rafraîchit les données
     */
    async refresh() {
        await this.loadData();
        this.notification.add("Données actualisées", {
            type: "success",
        });
    }
}

EazynovaDashboard.template = "eazynova.Dashboard";

registry.category("actions").add("eazynova.dashboard", EazynovaDashboard);