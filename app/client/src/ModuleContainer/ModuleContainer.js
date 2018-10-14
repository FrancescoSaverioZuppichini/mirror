import React, { Component } from 'react'
import { Container } from 'unstated';
import axios from 'axios'
import api from '../api.js'
import querystring from 'querystring'

class ModuleContainer extends Container {
    state = {
        tree: null,
        isLoading: true,
        open: false,
        outputs: [],
        layerId: null,
        last: 0
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

    getLayerOutputs = async (layerId) => {
        const last = layerId != this.state.layerId ? 0 : this.state.last + 25 
        console.log(last)
        const res = await axios.get(api.getModuleLayerOutput(layerId, last), { params : { last }})

        const outputs = res.data

        await this.setState({ outputs, layerId, last })

    }
}

export default ModuleContainer