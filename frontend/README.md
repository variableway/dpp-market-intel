# Frontend

Next.js App Router + Tailwind + shadcn 风格组件实现的前端。

当前默认是纯静态构建模式，页面构建时直接读取 `public/data/*.json`。

## 页面

- `/` Dashboard
- `/news` News

## 环境变量

当前静态模式不依赖运行时 API 环境变量。

## 启动

```bash
pnpm install
pnpm export:data
pnpm dev
```

## 构建静态站

```bash
pnpm build
```

输出目录：

```bash
out/
```
