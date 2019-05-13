<template>
    <div id="app">
        <el-container class="main-container">
<!--            <el-aside class="aside-navbar" width="240px">
                <AsideNavBar/>
            </el-aside>-->
            <el-main>
                <router-view/>
            </el-main>
        </el-container>
    </div>
</template>

<script>
// import AsideNavBar from '@/components/AsideNavBar'

export default {
    name: 'app',
    data() {
        return {
            activeName: window.location.pathname.slice(1),
        }
    },
    methods: {
        onTabClick(tab) {
            const tabName = tab.name
            this.$router.push(tabName)
        },
    },
    components: {},
}
</script>

<style>
html,body {
    height: 100%;
}
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    height: 100%;
}
.main-container{
    height: 100%;
}
.aside-navbar ul {
    height: 100%;
}
</style>
