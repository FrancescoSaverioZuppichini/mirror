import React, { Component } from 'react'
import { Container } from 'unstated';
import axios from 'axios'
import api from '../api.js'
import querystring from 'querystring'

class ModuleContainer extends Container {
    state = {
        tree: null,
        isLoading: false,
        open: false,
        outputs: [],
        layerId: null,
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

    getLayerOutputs = async (layerId=this.state.layerId) => {
        const isSameLayer = layerId == this.state.layerId
        const last = isSameLayer ? this.state.last + 64 : 0
        try {
            await this.setState({ isLoading: true })

            const res = await axios.get(api.getModuleLayerOutput(layerId, last), { params: { last } })
    
            var outputs = isSameLayer ? this.state.outputs.concat(res.data) : res.data
    
            await this.setState({ outputs, layerId, last, isLoading: false })
        } catch {
            await this.setState({ isLoading: false })
        }
    }

    changeSettings = async(settings) => {
        await this.setState( { settings })
    }
}

export default ModuleContainer