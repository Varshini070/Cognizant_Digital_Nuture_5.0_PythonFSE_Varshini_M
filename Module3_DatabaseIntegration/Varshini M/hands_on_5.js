db.feedback.countDocuments();

db.feedback.find({ rating: 5 });

db.feedback.find({ course_code: "CS101", tags: "challenging" });

db.feedback.find({}, { student_id: 1, course_code: 1, rating: 1, _id: 0 });

db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } },
);

db.feedback.updateMany({ needs_review: true }, { $push: { tags: "reviewed" } });

db.feedback.deleteMany({ semester: "2021-EVEN" });

db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      feedback_count: { $sum: 1 },
    },
  },
  { $sort: { avg_rating: -1 } },
]);

db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      feedback_count: { $sum: 1 },
    },
  },
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      average_rating: { $round: ["$avg_rating", 1] },
      feedback_count: 1,
    },
  },
  { $sort: { average_rating: -1 } },
]);

db.feedback.aggregate([
  {
    $unwind: "$tags",
  },
  {
    $group: {
      _id: "$tags",
      count: {
        $sum: 1,
      },
    },
  },
  {
    $sort: {
      count: -1,
    },
  },
]);

db.feedback.createIndex({ course_code: 1 });

//IXSCAN instead od COLLSCAN verified
