<template>
    <div class="home">
        <div>
            <h1>垃圾邮件识别系统</h1>
        </div>

        <el-row>
            <el-button-group style="float: left;">
                <el-button type="primary" @click="identifyMail" :loading="identifyButtonLoading" icon="el-icon-search">识别</el-button>
            </el-button-group>
        </el-row>

        <el-row>
            <el-col :span="24">
                <el-input type="textarea" v-model="mailContentToIdentify"
                          placeholder="请输入要识别的邮件正文（暂时只支持中文邮件）"
                          :autosize="{ minRows: 15, maxRows: 30}"></el-input>
            </el-col>
        </el-row>

        <el-row type="flex" justify="space-around">
            <el-col :span="10">
                <el-card :body-style="{padding: '0px'}" shadow="hover">
                    <div class="word_cloud_image spam" @click="viewImage('spam')"
                         v-viewer="{movable: false, navbar: false, toolbar: false}">
                        <el-image alt="垃圾邮件关键词词云" :src="spam_word_cloud_image_url" style="cursor: pointer;"
                        ></el-image>
                    </div>
                    <div style="padding: 14px">
                        <span><span style="color: #F01A23;">垃圾</span>邮件关键词词云</span>
                        <div class="bottom clearfix">
                            <el-button type="text" class="button" @click="viewImage('spam')">点击放大查看
                            </el-button>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="10">
                <el-card :body-style="{padding: '0px'}" shadow="hover">
                    <div class="word_cloud_image ham" @click="viewImage('ham')"
                         v-viewer="{movable: false, navbar: false, toolbar: false}">
                        <el-image alt="正常邮件关键词词集" :src="ham_word_cloud_image_url" style="cursor: pointer;"
                                  @click="viewImage(this)"></el-image>
                    </div>
                    <div style="padding: 14px">
                        <span><span style="color: #04E474;">正常</span>邮件关键词词云</span>
                        <div class="bottom clearfix">
                            <el-button type="text" class="button" @click="viewImage('ham')">点击放大查看
                            </el-button>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<style>
    .el-row {
        margin-bottom: 20px;
    }
</style>

<script>
import 'viewerjs/dist/viewer.css'
import {identifyMail} from '@/api'
import {isNil} from 'lodash'
import Viewer from 'v-viewer'
import Vue from 'vue'
import config from '@/config'

Vue.use(Viewer)

export default {
    name: 'home',
    data() {
        return {
            identifyButtonLoading: false,
            mailContentToIdentify: '',
            spam_word_cloud_image_url: config.backendApiUrlPrefix + '/wordcloud/spam',
            ham_word_cloud_image_url: config.backendApiUrlPrefix + '/wordcloud/ham',
        }
    },
    methods: {
        viewImage(wordCloudType) {
            const viewer = this.$el.querySelector('.word_cloud_image.' + wordCloudType).$viewer
            viewer.show()
        },
        identifyMail() {
            let mail = {
                content: this.mailContentToIdentify,
            }
            this.identifyButtonLoading = true
            identifyMail(mail)
                .then(res => {
                    console.log(res)
                    if (isNil(res.data)) {
                        this.$message.error('服务器返回了空的结果')
                    } else {
                        let resData = res.data
                        if (resData.success) {
                            this.$message.closeAll()
                            let message = '该邮件被判断为' + (resData.data.type === 'ham' ? '<span style="color: #04E474;">正常</span>邮件' : '<span style="color: #F01A23;">垃圾</span>邮件')
                            if (!isNil(resData.data.warnMessage)) {
                                message += '（' + resData.data.warnMessage + '）'
                            }
                            this.$message({
                                message: message,
                                dangerouslyUseHTMLString: true,
                                type: resData.data.type === 'ham' ? 'success' : 'warning',
                            })
                        } else {
                            this.$message.closeAll()
                            this.$message.error(resData.message)
                        }
                    }
                    this.identifyButtonLoading = false
                })
                .catch(err => {
                    this.$message.closeAll()
                    this.$message.error(String(err))
                    this.identifyButtonLoading = false
                })
        }
    }
}
</script>
