import React, { Component } from 'react'
import { Container } from 'unstated';
import axios from 'axios'
import api from '../api.js'
import querystring from 'querystring'

class ModuleContainer extends Container {
    state = {
        tree: null,
        visualisations: [],
        currentVisualisation: {},
        isLoading: false,
        open: false,
        outputs: [],
        layer: { name : ''},
        last: 0,
        next: false,
        settings: { size: 50 }
    }

    async getTree() {
        await this.setState({ isLoading: true })

        const res = await axios.get(api.GET_MODULE)
        const tree = res.data

        await this.setState({ tree, isLoading: false })
    }

    toogleDrawer = async () => {
        await this.setState({ open: !this.state.open })

    }

    getLayerOutputs = async (layer=this.state.layer, start=false) => {
        if(this.state.isLoading){
            console.log('Loading')
            return
        } 
        var isSameLayer = layer.id == this.state.layer.id
        if(start) isSameLayer = false
        var last = isSameLayer ? this.state.last + 64 : 0
        try {
            await this.setState({ isLoading: true })

            const res = await axios.get(api.getModuleLayerOutput(layer.id, last), { params: { last } })
    
            var outputs = isSameLayer ? this.state.outputs.concat(res.data.links) : res.data.links
            
            await this.setState({ outputs, layer, last, isLoading: false, next: res.data.next })
        } catch {
            await this.setState({ isLoading: false })
        }
    }

    changeSettings = async(settings) => {
        await this.setState( { settings })
    }

    async getVisualisations() {
        if(this.state.isLoading){
            console.log('Loading')
            return
        } 
        await this.setState({ isLoading: true })

        const res = await axios.get(api.GET_VISUALISATIONS)
        const visualisations = res.data.visualisations
        const currentVisualisation = res.data.current
        await this.setState({ visualisations, isLoading: false, currentVisualisation })
    }

    async setVisualisationsSettings(data){
        if(this.state.isLoading){
            console.log('Loading')
            return
        } 
        await this.setState({ isLoading: true })

        const res = await axios.put(api.PUT_VISUALISATIONS, data)

        const currentVisualisation = res.data
        var visualisations = [...this.state.visualisations]
        // TODO could be smarter!
        for(let key in visualisations){
            if(visualisations[key].name == currentVisualisation.name){
                visualisations[key] = currentVisualisation
            }
        }
        await this.setState({isLoading: false, currentVisualisation, visualisations })

    }


}

export default ModuleContainer