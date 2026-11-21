# pairwise-msaa-resolve

开启 4x MSAA 后，草地边缘出现一圈灰边，resolve 在 sRGB 空间做平均，亮暗样本被非线性压暗；alpha 覆盖没参与 resolve，半透明边缘的样本数被当成 4 个全不透明；模板缓冲只在样本 0 写入，resolve 后描边只剩四分之一个像素；深度 resolve 取平均，边缘像素深度落在几何之间，后处理把它当成前景；centroid 采样没开，像素中心落在三角形外时取到错误覆盖；HDR 颜色在 resolve 前做了色调映射，平均的是映射后的值，边缘发灰；UAV 直接读多重采样纹理，没走 resolve，读到未定义的样本；后处理链在 resolve 之前插入了降噪，降噪按单样本处理导致锯齿；VR 双眼各自 resolve 但共用一张纹理，左眼的样本被右眼覆盖；MSAA 与 TAA 同时开启，TAA 历史缓冲按单样本存储，两者互相抵消。render/msaa_resolve.py 是核心，tests/test_msaa_resolve.py 15个红。要修的是：线性空间 resolve；alpha 按覆盖加权；模板逐样本写；深度取最近样本；centroid 采样；先 resolve 再映射；UAV 走 resolve；后处理放到 resolve 后；双眼独立纹理；MSAA 与 TAA 分工。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：见平台；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
