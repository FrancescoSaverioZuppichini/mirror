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

    getLayerOutputs = async (layer=this.state.layer) => {
        const isSameLayer = layer.id == this.state.layer.id
        const last = isSameLayer ? this.state.last + 64 : 0
        try {
            await this.setState({ isLoading: true })

            const res = await axios.get(api.getModuleLayerOutput(layer.id, last), { params: { last } })
    
            var outputs = isSameLayer ? this.state.outputs.concat(res.data) : res.data
    
            await this.setState({ outputs, layer, last, isLoading: false })
        } catch {
            await this.setState({ isLoading: false })
        }
    }

    changeSettings = async(settings) => {
        await this.setState( { settings })
    }

    async getVisualisations() {
        await this.setState({ isLoading: true })

        const res = await axios.get(api.GET_VISUALISATIONS)
        const visualisations = res.data

        await this.setState({ visualisations, isLoading: false })
    }

    async setVisualisationsSettings(data){

        await this.setState({ isLoading: true })

        const res = await axios.put(api.PUT_VISUALISATIONS, data)

        const currentVisualisation = res.data
        var visualisations = [...this.state.visualisations]

        console.log(visualisations)

        for(let key in visualisations){
            if(visualisations[key].name == currentVisualisation.name){
                visualisations[key] = currentVisualisation
            }
        }

        console.log(visualisations)

        await this.setState({isLoading: false, currentVisualisation, visualisations })

    }


}

export default ModuleContainer