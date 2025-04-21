import {createApp} from 'vue'
import "@pdn-certic/vue3-jama/dist/style.css";
import {VueJamaPlugin, VueJamaApp} from "@pdn-certic/vue3-jama";
import 'vuetify/styles'

const withAnnotations : boolean = Number(import.meta.env.VITE_ANNOTATIONS_ENABLED) != 0

let jamaOptions: any = {
    title: 'Jama UI',
}

if(withAnnotations){
    jamaOptions.annotableImages = {
        basePath: '/static/ui/'
    }
}
else {
    jamaOptions.annotableImages = false
}

const app = createApp(VueJamaApp, jamaOptions);
app.use(VueJamaPlugin, true)
app.mount('#app')
