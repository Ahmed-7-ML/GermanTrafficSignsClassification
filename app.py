if choice == "Enhance Image":
    enhancement_choice = st.selectbox("Choose Enhancement", 
            ["Negative", "Add Tint", "Crop", "Adjust Brightness",
            "Adjust Contrast", "Grayscale", "Add Shape", "Add Text",
            "Histogram Equalization", "Scale", "Translate",
            "Rotate", "Blur", "Sharpen", "Edge Detection"])

    manipulator = ImageManipulations(uploaded_file)

    if enhancement_choice == "Negative":
        manipulator.negative()

    elif enhancement_choice == "Add Tint":
        color = st.color_picker("Pick a tint color", value="#ff0000")
        intensity = st.slider("Select Tint Intensity", 0.0, 1.0, 0.5)
        manipulator.add_tint(color=tuple(
            int(color[i:i+2], 16) for i in (1, 3, 5)), intensity=intensity)

    elif enhancement_choice == "Crop":
        left = st.number_input("Left", min_value=0, value=0)
        top = st.number_input("Top", min_value=0, value=0)
        right = st.number_input("Right", min_value=0, value=image.width)
        bottom = st.number_input("Bottom", min_value=0, value=image.height)
        manipulator.crop((left, top, right, bottom))

    elif enhancement_choice == "Adjust Brightness":
        factor = st.slider("Brightness factor", 0.0, 5.0, 1.5)
        manipulator.adjust_brightness(factor)

    elif enhancement_choice == "Adjust Contrast":
        factor = st.slider("Contrast factor", 0.0, 5.0, 1.5)
        manipulator.adjust_contrast(factor)

    elif enhancement_choice == "Grayscale":
        manipulator.to_grayscale()

    elif enhancement_choice == "Add Shape":
        shape = st.selectbox("Shape", ["circle", "rectangle"])
        position = (st.slider("Position X", 0, image.width),
                    st.slider("Position Y", 0, image.height))
        size = st.slider("Size", 10, 200, 50)
        color = st.color_picker("Pick a shape color", value="#ff0000")
        manipulator.add_shape(shape=shape, position=position, size=size, color=tuple(int(color[i:i+2], 16) for i in (1, 3, 5)))

    elif enhancement_choice == "Add Text":
        text = st.text_input("Text", "Sample Text")
        position = (st.slider("Text Position X", 0, image.width),
                    st.slider("Text Position Y", 0, image.height))
        color = st.color_picker("Pick text color", value="#ffffff")
        manipulator.add_text(text=text, position=position, color=tuple(
            int(color[i:i+2], 16) for i in (1, 3, 5)))

    elif enhancement_choice == "Histogram Equalization":
        manipulator.histogram_equalization()

    elif enhancement_choice == "Scale":
        width = st.slider("Width", 10, image.width * 2, image.width)
        height = st.slider("Height", 10, image.height * 2, image.height)
        manipulator.scale(width=width, height=height)

    elif enhancement_choice == "Translate":
        x = st.slider("Translation X", -image.width, image.width, 0)
        y = st.slider("Translation Y", -image.height, image.height, 0)
        manipulator.translate(x, y)

    elif enhancement_choice == "Rotate":
        angle = st.slider("Rotation Angle", 0, 360, 0)
        manipulator.rotate(angle)

    elif enhancement_choice == "Blur":
        manipulator.blur()

    elif enhancement_choice == "Sharpen":
        manipulator.sharpen()

    elif enhancement_choice == "Edge Detection":
        manipulator.edge_detection()

    # Show the manipulated image
    st.image(manipulator.manipulated,
        caption="Enhanced Image", use_column_width=True)

    # Option to save the manipulated image
    save_button = st.button("Save Enhanced Image")
    if save_button:
        output_path = "enhanced_image.jpg"
        manipulator.save(output_path)
        st.success(f"Enhanced image saved as {output_path}")

elif choice == "Predict Image":
    prediction = predict_image(image)
    st.write(f"Prediction: {prediction[0]}")  # Show Decision Tree prediction
