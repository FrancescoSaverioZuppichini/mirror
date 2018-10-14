import React, { Component } from 'react'
import { Container } from 'unstated';
import axios from 'axios'
import api from '../api.js'

class ModuleContainer extends Container {
    state = {
        tree : undefined,
        isLoading: true,
        open: false
    }

    async getTree() {
        await this.setState({ isLoading: true })

        const res = await axios.get(api.GET_MODULE)
        const tree = res.data

        await this.setState({ tree, isLoading: false })
    }

    toogleDrawer = async() => {
        await this.setState({ open : !this.state.open })

    }
}

export default ModuleContainer