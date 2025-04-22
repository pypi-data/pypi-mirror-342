# Example usage:
```
with open("data/labels.json", "r") as f:
    metadata = json.load(f)

label_map, angle_map = build_label_maps(metadata)

X, y, angles = build_dataset(
    metadata=metadata,
    clip_dir=Path("data"),
    label_to_idx=label_map,
    angle_to_idx=angle_map,
    max_people=2,
    target_len=60,
    fill_mode="last"
)

save_dataset(X, y, angles, Path("data/dataset.npz"))
save_label_maps(label_map, angle_map, Path("data"))
```