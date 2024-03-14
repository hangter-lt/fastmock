import React, { useState, useEffect, useRef } from 'react';
import { Layout, Tree, theme, Switch, Empty, Tag, Button, Tooltip, Popconfirm, Modal, Form, Input } from 'antd';
import type { DataNode } from 'antd/es/tree';
import axios from 'axios';
import { MdEditor, ToolbarNames } from 'md-editor-rt';
import 'md-editor-rt/lib/style.css';
import { API_TREE, API_FILE, API_FILES_WRITE, API_FILES_ADD, API_FILES_RENAME, API_FILES_REMOVE } from '../consts';
import { DeleteOutlined, FileAddOutlined, EditOutlined } from '@ant-design/icons';

const { Content, Sider } = Layout;

const ApiFiles: React.FC = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    const [showIcon, setShowIcon] = useState<boolean>(false);

    const [tree, setTree] = useState<DataNode[]>([])

    const [content, setContent] = useState("")

    const [renameModalOpen, setRenameModalOpen] = useState(false);
    const [createModalOpen, setCreateModalOpen] = useState(false);
    const [createProModalOpen, setCreateProModalOpen] = useState(false);
    const [updateTree, setUpdateTree] = useState(false)

    const [path, setPath] = useState("")

    // 当前操作节点
    const currentNode = useRef({ "key": "", "title": "" })

    // 重命名表单
    const [rename] = Form.useForm()
    // 新建表单
    const [create] = Form.useForm()

    const toolbars: ToolbarNames[] | undefined = [
        'save',
        'unorderedList',
        'codeRow',
        'code',
        '=',
        'pageFullscreen',
        'fullscreen',
        'preview',
        'catalog',
    ];


    const setFileTitle = (title: any): any => {
        return (
            <span>
                {title}
                <Tooltip title="重命名">
                    <Button type="text" icon={<EditOutlined />} onClick={showRenameModal} />
                </Tooltip>
                <Tooltip title="删除文件">
                    <Popconfirm
                        title="确认删除?"
                        onConfirm={deleteConfirm}
                        okText="是"
                        cancelText="否"
                    >
                        <Button type="text" icon={<DeleteOutlined />} />
                    </Popconfirm>
                </Tooltip>
            </span>
        )
    }

    const setFolderTitle = (title: any): any => {
        return (
            <span>{title}
                <Tooltip title="新建">
                    <Button type="text" icon={<FileAddOutlined />} onClick={showCreateModal} />
                </Tooltip>
                <Tooltip title="重命名">
                    <Button type="text" icon={<EditOutlined />} onClick={showRenameModal} />
                </Tooltip>
                <Tooltip title="删除目录">
                    <Popconfirm
                        title="确认删除?"
                        onConfirm={() => deleteConfirm()}
                        okText="是"
                        cancelText="否"
                    >
                        <Button type="text" icon={<DeleteOutlined />} />
                    </Popconfirm>
                </Tooltip>
            </span>
        )
    }

    const fillButton = (datas: any[]) => {
        for (var i = 0; i < datas.length; i++) {
            if (datas[i].type == "file") {
                datas[i].title = setFileTitle(datas[i].title)
            } else {
                datas[i].title = setFolderTitle(datas[i].title)
            }
            if (datas[i].children != null) {
                fillButton(datas[i].children)
            }
        }
    }

    const getTree = () => {
        axios.get(API_TREE).then((res) => {
            let datas: DataNode[] = res.data

            // 递归填充树节点按钮
            fillButton(datas)
            setTree(datas)
        })
    }


    // @ts-ignore
    // 选中树节点时
    const select = (selectedKeys: any, e: {
        event: 'select';
        selected: boolean;
        node: any;
        selectedNodes: any;
        nativeEvent: MouseEvent;
    }) => {

        currentNode.current = {
            "key": e.node.key,
            "title": e.node.title.props.children[0]
        }
        rename.setFieldValue("name", e.node.title.props.children[0])
        // console.log(key)
        // console.log(title)
        if (e.node.type == "file") {
            axios.get(API_FILE + e.node.key).then((res) => {
                setContent(res.data)
                setPath(e.node.key)
            })
        }
    }

    const change = (v: string) => {
        setContent(v)
    }

    // @ts-ignore
    const save = (v: string, h: Promise<string>) => {
        axios.post(API_FILES_WRITE, {
            "path": path,
            "file": content,
        }).then((res) => {
            console.log(res)
        })
    }

    useEffect(() => {
        getTree()
    }, [updateTree]);


    const showRenameModal = () => {
        setRenameModalOpen(true);
    };

    const handleRenameCancel = () => {
        setRenameModalOpen(false);
    };

    const renameFinish = (values: any) => {
        axios.post(API_FILES_RENAME, {
            "key": currentNode.current.key,
            "name": values.name,
        }).then((res) => {
            console.log(res)
            setUpdateTree(!updateTree)
            setRenameModalOpen(false)
        }) 
    };

    const showCreateModal = () => {
        setCreateModalOpen(true)
    }

    const handleCreateCancel = () => {
        setCreateModalOpen(false)
    }

    const createFinish = (values: any) => {
        axios.post(API_FILES_ADD, {
            "key": currentNode.current.key,
            "name": values.name,
            "is_dir": values.is_dir,
        }).then((res) => {
            console.log(res)
            setUpdateTree(!updateTree)
            setCreateModalOpen(false)
        })
    }

    const showCreateProModal = () => {
        setCreateProModalOpen(true)
    }

    const handleCreateProCancel = () => {
        setCreateProModalOpen(false)
    }

    const createProFinish = (values: any) => {
        console.log(values)
        axios.post(API_FILES_ADD, {
            "key": "",
            "name": values.name,
            "is_dir": true,
        }).then((res) => {
            console.log(res)
            setUpdateTree(!updateTree)
            setCreateProModalOpen(false)
        }) 
    }

    const deleteConfirm = () => {
        console.log(currentNode.current);
        axios.post(API_FILES_REMOVE, {
            "key": currentNode.current.key,
        }).then((res) => {
            console.log(res)
            setUpdateTree(!updateTree)
        })
    };

    return (
        <Layout style={{ background: colorBgContainer, height: '100%', padding: '10px 0px' }}>
            <Modal title="重命名" open={renameModalOpen} onCancel={handleRenameCancel} footer="">
                <Form
                    form={rename}
                    name="rename"
                    onFinish={renameFinish}
                >
                    <Form.Item
                        name="name">
                        <Input />
                    </Form.Item>

                    <Form.Item >
                        <Button type="primary" htmlType="submit">
                            确认
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal title="新建文件" open={createModalOpen} onCancel={handleCreateCancel} footer="">
                <Form
                    form={create}
                    name="create"
                    onFinish={createFinish}
                >
                    <Form.Item
                        name="name">
                        <Input placeholder='请输入文件名或目录名' />
                    </Form.Item>

                    <Form.Item
                        name="is_dir">
                        <Switch checkedChildren="新建目录" unCheckedChildren="新建文件" />
                    </Form.Item>

                    <Form.Item >
                        <Button type="primary" htmlType="submit">
                            确认
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal title="新建项目" open={createProModalOpen} onCancel={handleCreateProCancel} footer="">
                <Form
                    name="createPro"
                    onFinish={createProFinish}
                >
                    <Form.Item
                        name="name">
                        <Input placeholder='请输入项目名称' />
                    </Form.Item>

                    <Form.Item >
                        <Button type="primary" htmlType="submit">
                            确认
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>



            <Sider style={{ background: colorBgContainer, overflow: 'auto' }} width={300}>
                <Switch style={{ display: 'none' }} checked={showIcon} onChange={setShowIcon} />
                <Button onClick={showCreateProModal}>新建项目</Button>
                <Tree
                    showIcon={showIcon}
                    treeData={tree}
                    onSelect={select}
                />

            </Sider>
            {path == "" && (
                <Empty style={{ margin: 200 }} description={false} />
            )}
            {path != "" && (
                <Content style={{ padding: '30px 30px' }}>
                    <MdEditor
                        toolbars={toolbars}
                        modelValue={content}
                        style={{ height: "100%" }}
                        onSave={save}
                        onChange={change}
                    />
                    <Tag color='red' bordered={false}>单机左上角按钮或输入Ctrl+S保存</Tag>
                </Content>
            )}
        </Layout >
    );
};

export default ApiFiles;