import React, { Component } from 'react'
import { Container } from 'unstated';
import axios from 'axios'
import api from '../api.js'

class ModuleContainer extends Container {
    state = {
        tree : undefined
    }

    async getTree() {
        const res = await axios.get(api.GET_MODULE)
        const tree = res.data

        // const tree = {'diocane': []}
        this.setState({ tree })
    }
}

export default ModuleContainer