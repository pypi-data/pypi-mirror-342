<script lang="ts">
    import { onMount, createEventDispatcher } from "svelte";
	import AnnotatedImageData from "./AnnotatedImageData";	

    export let value: null | AnnotatedImageData;
    export let src: string | null = null;
    export let interactive: boolean = true;
    export let height: number | string = "100%";
    export let width: number | string = "100%";
    export let imgSize: number | null = null;
    export let patchSize: number = 16;
    export let showGrid: boolean = true;
    export let gridColor: string = "rgba(200, 200, 200, 0.5)";
    
    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    let image: HTMLImageElement | null = null;
    let imageWidth = 0;
    let imageHeight = 0;
    let canvasXmin = 0;
    let canvasYmin = 0;
    let scaleFactor = 1.0;
    let effectiveWidth = 0;
    let effectiveHeight = 0;
    let gridScaleX = 1.0;
    let gridScaleY = 1.0;
    
    const dispatch = createEventDispatcher<{
        patch_select: object;
    }>();
    
    function drawGrid() {
        if (!ctx || !image || !showGrid) return;

        ctx.save();
        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 1;
        
        // Calculate grid dimensions using shared variables
        const gridWidth = Math.floor(effectiveWidth / patchSize);
        const gridHeight = Math.floor(effectiveHeight / patchSize);
        console.log(`[PatchSelector.svelte:drawGrid] patch size: ${patchSize}`);
        
        // Draw horizontal lines
        for (let i = 0; i <= gridHeight; i++) {
            const y = canvasYmin + (i * patchSize * gridScaleY);
            ctx.beginPath();
            ctx.moveTo(canvasXmin, y);
            ctx.lineTo(canvasXmin + imageWidth, y);
            ctx.stroke();
        }
        
        // Draw vertical lines
        for (let i = 0; i <= gridWidth; i++) {
            const x = canvasXmin + (i * patchSize * gridScaleX);
            ctx.beginPath();
            ctx.moveTo(x, canvasYmin);
            ctx.lineTo(x, canvasYmin + imageHeight);
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    function handleImageLoad() {
        if (!canvas) return;
        console.debug("[PatchSelector.svelte:handleImageLoad] Image loaded"); 
        ctx = canvas.getContext("2d");
        
        // Set canvas dimensions based on image
        scaleFactor = 1;
        canvas.width = canvas.clientWidth;
        
        if (image !== null) {
            // Use imgSize if provided, otherwise use the natural dimensions
            effectiveWidth = imgSize || image.width;
            effectiveHeight = imgSize || image.height;
            
            if (imgSize) {
                // If imgSize is provided, use a square dimension
                effectiveWidth = imgSize;
                effectiveHeight = imgSize;
            }
            
            if (effectiveWidth > canvas.width) {
                scaleFactor = canvas.width / effectiveWidth;
                imageWidth = effectiveWidth * scaleFactor;
                imageHeight = effectiveHeight * scaleFactor;
                canvasXmin = 0;
                canvasYmin = 0;
            } else {
                imageWidth = effectiveWidth;
                imageHeight = effectiveHeight;
                canvasXmin = (canvas.width - imageWidth) / 2;
                canvasYmin = 0;
            }
            canvas.height = imageHeight;
            
            // Calculate grid scale factors once
            gridScaleX = imageWidth / effectiveWidth;
            gridScaleY = imageHeight / effectiveHeight;
        } else {
            canvas.height = canvas.clientHeight;
        }
        
        draw();
    }
    
    function draw() {
        if (!ctx) return;
        
        console.debug("Drawing on canvas");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        if (image !== null) {
            // Draw the image
            console.debug(`[PatchSelector.svelte:draw] Drawing image`);
            console.debug(`[PatchSelector.svelte:draw] image dimensions: ${image.width}x${image.height}:${imgSize}`);
            console.debug(`[PatchSelector.svelte:draw] image sizes: ${imageWidth}x${imageHeight}:${imgSize}`);
            console.debug(`[PatchSelector.svelte:draw] effective image sizes: ${effectiveWidth}x${effectiveHeight}:${imgSize}`);

            ctx.drawImage(image, canvasXmin, canvasYmin, imageWidth, imageHeight);
            
            console.debug("Drawing grid");
            // Draw the grid overlay
            drawGrid();
        }
    }
    
    function handleClick(event: MouseEvent) {
        if (!interactive || !image) return;
        
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        
        // Calculate which grid cell/patch was clicked using shared variables
        const x = Math.floor((mouseX - canvasXmin) / (patchSize * gridScaleX));
        const y = Math.floor((mouseY - canvasYmin) / (patchSize * gridScaleY));
        
        // Calculate the grid dimensions
        const gridWidth = Math.floor(effectiveWidth / patchSize);
        
        // Calculate the linear patch index (row-major order)
        const patchIndex = y * gridWidth + x;
        
        // Only dispatch if the click is within the image bounds
        if (x >= 0 && x < gridWidth && y >= 0 && y < Math.floor(effectiveHeight / patchSize)) {
            // Highlight the selected patch
            highlightPatch(x, y);
            console.debug("[PatchSelector.svelte:handleClick] Patch index:", patchIndex); 
            // Dispatch the patch_select event with the patch index
            value.patchIndex = patchIndex;
            dispatch("patch_select", { patchIndex });
        }
    }
    
    function highlightPatch(gridX: number, gridY: number) {
        if (!ctx || !image) return;
        
        // Clear the previous drawing
        draw();
        
        // Highlight the selected patch using shared variables
        ctx.save();
        ctx.fillStyle = "rgba(255, 255, 0, 0.2)";
        ctx.fillRect(
            canvasXmin + gridX * patchSize * gridScaleX,
            canvasYmin + gridY * patchSize * gridScaleY,
            patchSize * gridScaleX,
            patchSize * gridScaleY
        );
        ctx.restore();
    }
    
    // Update imgSize and patchSize when they change in the value object
    $: if (value?.imgSize !== undefined && value.imgSize !== null) {
        console.log(`[PatchSelector.svelte] Changing patch size: ${imgSize} -> ${value.imgSize}`);
        imgSize = value.imgSize;
    }
    
    $: if (value?.patchSize !== undefined && value.patchSize !== null) {
        console.log(`[PatchSelector.svelte] Changing patch size: ${patchSize} -> ${value.patchSize}`);
        patchSize = value.patchSize;
    }
    
    // Redraw when patch size or image size changes
    $: if (image && (patchSize || imgSize)) {
        console.log(`[PatchSelector.svelte] Redrawing canvas with new patch size: ${patchSize}`);
        handleImageLoad();
    }
    
    $: if (src) {
        image = new Image();
        image.src = src;
        image.onload = handleImageLoad;
    }
    
    onMount(() => {
        if (image && image.complete) {
            handleImageLoad();
        }
    });
</script>

<div class="patch-selector-container">
    <canvas
        bind:this={canvas}
        on:click={handleClick}
        style="height: {height}; width: {width};"
        class="patch-selector-canvas"
    ></canvas>
</div>

<style>
    .patch-selector-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .patch-selector-canvas {
        border-color: var(--block-border-color);
        width: 100%;
        height: 100%;
        display: block;
        touch-action: none;
    }
</style>
