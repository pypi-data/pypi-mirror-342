import {defineConfig} from 'vite'
import autoprefixer from 'autoprefixer'
import {fileURLToPath, URL} from 'node:url'
import path from 'node:path'

export default defineConfig(({command, mode, isSsrBuild, isPreview}) => {
    console.log('Config arguments:', command, mode, isSsrBuild, isPreview)

    //+----------+-------+-------------+-------+-------+
    //| dev:     | serve | development | false | false
    //| preview: | serve | production  | false | true
    //| build:   | build | production  | false | false
    //+----------+-------+-------------+-------+-------+

    const common = {
        root: path.resolve(__dirname, './src'),
        publicDir: path.resolve(__dirname, './public'),
        minify: mode === 'development' ? false : 'terser',
        resolve: {
            extensions: ['.js', '.scss'],
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                'templates': fileURLToPath(new URL('./src/templates', import.meta.url)),
                'components': fileURLToPath(new URL('./src/templates/components', import.meta.url)),
                'containers': fileURLToPath(new URL('./src/templates/containers', import.meta.url)),
                'layouts': fileURLToPath(new URL('./src/templates/layouts', import.meta.url)),
                'views': fileURLToPath(new URL('./src/templates/views', import.meta.url)),
                'static': fileURLToPath(new URL('./src/static', import.meta.url)),
                'scss': fileURLToPath(new URL('./src/static/scss', import.meta.url)),
                'fonts': fileURLToPath(new URL('./src/static/fonts', import.meta.url)),
                'media': fileURLToPath(new URL('./src/static/media', import.meta.url)),
                'js': fileURLToPath(new URL('./src/static/js', import.meta.url))
            }
        }
    }

    if (command === 'serve') {
        return {
            // dev specific config
            base: '/',
            server: {
                open: true,
                hmr: {
                    overlay: true
                },
                warmup: {
                    clientFiles: [
                        './src/**/*.scss'
                    ]
                }
            },
            css: {
                devSourcemap: true,
                postcss: {
                    plugins: [
                        autoprefixer()
                    ]
                }
            },
            sourcemap: 'inline',
            ...common
        }
    } else {
        // command === 'build'
        return {
            // build specific config
            base: './',
            preview: {
                open: true
            },
            sourcemap: false,
            build: {
                outDir: path.resolve(__dirname, './build'),
                emptyOutDir: true,
                manifest: 'manifest.json',
                rollupOptions: {
                    input: {
                        main: path.resolve(__dirname, './src/index.html')
                    },
                    output: {
                        entryFileNames: 'js/[name].[hash].js',
                        chunkFileNames: 'js/[name].[hash].js',
                        assetFileNames: (assetInfo => {
                            const info = assetInfo.name.split('.')
                            let ext = info[info.length - 1]
                            if (/png|jpe?g|svg|gif|tiff|bmp|ico|webp|webm|mp3|wav/i.test(ext)) {
                                ext = 'media'
                            } else if (/(sa|sc|c)ss/i.test(ext)) {
                                ext = 'css'
                            } else if (/woff(2)?|eot|ttf|otf/i.test(ext)) {
                                ext = 'fonts'
                            } else ext = ''
                            return `${ext}/[name].[hash][extname]`
                        })
                    }
                }
            },
            ...common
        }
    }
})
