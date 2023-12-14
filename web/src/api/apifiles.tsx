import React, { useState, useEffect } from 'react';
import { Layout, Tree, theme, Switch, Empty, Tag, Menu, Dropdown } from 'antd';
import type { DataNode } from 'antd/es/tree';

import axios from 'axios';
import { MdEditor, ToolbarNames } from 'md-editor-rt';
import 'md-editor-rt/lib/style.css';
import { API_TREE, API_FILE, API_FILES_WRITE } from '../consts';


const { Content, Sider } = Layout;

const ApiFiles: React.FC = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    const [showIcon, setShowIcon] = useState<boolean>(false);

    const [tree, setTree] = useState<DataNode[]>([])

    const [content, setContent] = useState("")

    const [path, setPath] = useState("")

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

    const treeTitleAddDropdown = (childrens: DataNode[]) => {
        childrens.forEach((value: DataNode, index: number, array: DataNode[]) => {
            array[index].title = (
                <Dropdown  trigger={['contextMenu']}>
                    <div className="f12 tree-title">{value.title?.toString()}</div>
                </Dropdown>
            )
            if (value.children) {
                treeTitleAddDropdown(value.children)
            }
        })
    }

    const getTree = () => {
        axios.get(API_TREE).then((res) => {
            let datas: DataNode[] = res.data
            treeTitleAddDropdown(datas)
            console.log(datas)
            setTree(datas)
        })
    }

    // @ts-ignore
    const select = (selectedKeys: any, e: {
        event: 'select';
        selected: boolean;
        node: any;
        selectedNodes: any;
        nativeEvent: MouseEvent;
    }) => {
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
    }, []);

    const treeRightClickHandle = (info: {
        event: React.MouseEvent;
        node: any;
    }) => {
        info.event.preventDefault();
        console.log("123")
        //     const {dataRef} = node || {};
        //     const {itemType, operFlag, xrefStatus, key} = dataRef || {};
        //     setItemType(isMode(itemType)); // 显示右键菜单类型判断
        //     setNested(operFlag < 1 ? true : false); // 右键菜单项是否禁用标识
        //     setIsDisabled(xrefStatus == 4 ? true : false); // 某些指定的右键菜单项是否禁用标识
        //     setSelectTreeNode(dataRef);
        //     setSelectKeys([key]);
    }

    const items: any = [
        {
            label: "新建文件",
            key: "new",
        }
    ]
    const rightMenu = () => {
        return (
            <Menu items={items}></Menu>
        )
    }

    return (
        <Layout style={{ background: colorBgContainer, height: '100%', padding: '10px 0px' }}>
            <Sider style={{ background: colorBgContainer, overflow: 'auto' }} width={300}>
                <Switch style={{ display: 'none' }} checked={showIcon} onChange={setShowIcon} />

                <Tree
                    showIcon={showIcon}
                    treeData={tree}
                    onSelect={select}
                    onRightClick={({ event, node }) => treeRightClickHandle({ event, node })}
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